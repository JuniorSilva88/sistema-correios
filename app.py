from flask import Flask, render_template, request, redirect, url_for, Response, abort, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///correios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "segredo"  # necessário para sessões do Flask-Login

db = SQLAlchemy(app)
migrate = Migrate(app, db) 

# ---------------------------
# Login Manager e Decoradores
# ---------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            abort(403)  # acesso negado
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# Modelos
# ---------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # novo campo
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # "user" ou "admin"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(20), unique=True, nullable=False)
    sender = db.Column(db.String(100))
    recipient = db.Column(db.String(100))
    description = db.Column(db.String(200))
    status = db.Column(db.String(50))
    closed = db.Column(db.DateTime, nullable=True)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(20), db.ForeignKey('item.protocol'))
    type = db.Column(db.String(20))  # Entrada ou Saída
    location = db.Column(db.String(100))
    note = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)

# ---------------------------
# Rotas
# ---------------------------
@app.route("/")
@login_required
def index():
    items = Item.query.all()
    return render_template("dashboard.html", items=items)

@app.route("/new_item", methods=["GET", "POST"])
@login_required
def new_item():
    if request.method == "POST":
        protocol = f"{datetime.now().year}-{Item.query.count()+1:04d}"

        item = Item(
            protocol=protocol,
            sender=request.form["sender"],
            recipient=request.form["recipient"],
            description=request.form["description"],
            status="Em trânsito",
            closed=None
        )
        db.session.add(item)

        move = Movement(
            protocol=protocol,
            type="Entrada",
            location="Cadastro inicial",
            note="",
            created_at=datetime.now()
        )
        db.session.add(move)

        db.session.commit()
        return redirect(url_for("index"))
    return render_template("new_item.html")

@app.route("/movements/<protocol>")
@login_required
def movements(protocol):
    item = Item.query.filter_by(protocol=protocol).first()
    item_moves = Movement.query.filter_by(protocol=protocol).all()
    return render_template("movements.html", item=item, moves=item_moves)

@app.route("/movimentacoes")
@admin_required
def movimentacoes():
    movements = Movement.query.all()
    return render_template("movimentacoes.html", movements=movements)

@app.route("/exit_item/<protocol>", methods=["GET", "POST"])
@login_required
def exit_item(protocol):
    item = Item.query.filter_by(protocol=protocol).first()
    if request.method == "POST" and item:
        timestamp = datetime.now()

        move = Movement(
            protocol=protocol,
            type="Saída",
            location=request.form["location"],
            note=request.form["note"],
            created_at=timestamp
        )
        db.session.add(move)

        item.status = "Finalizado"
        item.closed = timestamp

        db.session.commit()
        return redirect(url_for("index"))
    return render_template("exit_item.html", item=item)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha inválidos!", "error")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/create_user", methods=["GET", "POST"])
@admin_required
def create_user():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form.get("role", "user")

        # Verifica duplicidade
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Usuário ou e-mail já existe!", "error")
            return redirect(url_for("create_user"))

        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Usuário criado com sucesso!", "success")
        return redirect(url_for("create_user"))

    return render_template("create_user.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu com sucesso.", "success")
    return redirect(url_for("login"))

@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    filtered = []

    if request.method == "POST":
        recipient = request.form.get("recipient")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        query = Item.query

        if recipient and recipient != "Todos":
            query = query.filter_by(recipient=recipient)

        if start_date and end_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_dt = end_dt.replace(hour=23, minute=59, second=59)

            # Apenas itens com fechamento dentro do intervalo
            query = query.filter(Item.closed.between(start_dt, end_dt))

        filtered = query.all()

    recipients = [r[0] for r in db.session.query(Item.recipient).distinct().all()]
    recipients.insert(0, "Todos")

    return render_template("report.html", items=filtered, sections=recipients)

@app.route("/report_csv", methods=["POST"])
@login_required
def report_csv():
    recipient = request.form.get("recipient")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    query = Item.query
    if recipient and recipient != "Todos":
        query = query.filter_by(recipient=recipient)

    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        end_dt = end_dt.replace(hour=23, minute=59, second=59)

        # Apenas itens com fechamento dentro do intervalo
        query = query.filter(Item.closed.between(start_dt, end_dt))

    items = query.all()

    lines = ["Protocolo,Descrição,Status,Remetente,Destinatário,Fechamento"]
    for item in items:
        closed = item.closed.strftime("%Y-%m-%d %H:%M:%S") if item.closed else ""
        lines.append(f"{item.protocol},{item.description},{item.status},{item.sender},{item.recipient},{closed}")

    csv_data = "\n".join(lines)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=relatorio.csv"}
    )

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        if current_user.check_password(old_password):
            current_user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash("Senha alterada com sucesso!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Senha atual incorreta!", "error")

    return render_template("change_password.html")

# ---------------------------
# Inicialização
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
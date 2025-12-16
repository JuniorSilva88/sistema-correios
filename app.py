from flask import Flask, render_template, request, redirect, url_for, Response, abort, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from flask_migrate import Migrate
from flask_mail import Mail, Message
import uuid 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///correios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "segredo"  # necessário para sessões do Flask-Login
app.config['MAIL_SERVER'] = 'smtp.seuprovedor.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seuemail@dominio.com'
app.config['MAIL_PASSWORD'] = 'suasenha'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # ⏳ 30 minutos de inatividade

mail = Mail(app)
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
            flash("Acesso restrito a administradores.", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# Modelos
# ---------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # "user" ou "admin"

    def set_password(self, password):
        # 🔐 usa pbkdf2:sha256 com salt e 260 mil iterações
        self.password_hash = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=16
        )

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
    protocol = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # Entrada ou Saída
    location = db.Column(db.String(100))
    note = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    user = db.Column(db.String(50), nullable=False)  # Novo campo: usuário responsável

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
        protocol = str(uuid.uuid4())[:8]
        item = Item(
            protocol=protocol,
            sender=request.form["sender"],
            recipient=request.form["recipient"],
            description=request.form["description"],
            status="Em trânsito"
        )
        db.session.add(item)

        move = Movement(
            protocol=protocol,
            type="Entrada",
            location="Cadastro inicial",
            note="Item cadastrado",
            created_at=datetime.now(),
            user=current_user.username  # grava quem fez
        )
        db.session.add(move)
        db.session.commit()

        flash("Item cadastrado com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("new_item.html")


@app.route("/exit_item/<protocol>", methods=["GET", "POST"])
@login_required
def exit_item(protocol):
    item = Item.query.filter_by(protocol=protocol).first_or_404()

    if request.method == "POST":
        item.status = "Finalizado"
        item.closed = datetime.now()

        move = Movement(
            protocol=protocol,
            type="Saída",
            location=request.form["location"],
            note=request.form.get("note", ""),
            created_at=datetime.now(),
            user=current_user.username  # grava quem fez
        )
        db.session.add(move)
        db.session.commit()

        flash("Saída registrada com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("exit_item.html", item=item)

@app.route("/create_admin")
def create_admin():
    # verifica se já existe admin
    existing_admin = User.query.filter_by(username="admin").first()
    if existing_admin:
        return "⚠️ Usuário admin já existe!", 400

    # cria novo admin
    admin = User(username="admin", email="admin@dominio.com", role="admin")
    admin.set_password("1234")  # senha padrão

    db.session.add(admin)
    db.session.commit()

    return "✅ Usuário admin criado com sucesso! Login: admin / Senha: 1234"


@app.route("/movimentacoes")
@login_required
def movimentacoes():
    query = Movement.query

    # filtro por usuário
    user_filter = request.args.get("user")
    if user_filter:
        query = query.filter_by(user=user_filter)

    # filtro por tipo
    type_filter = request.args.get("type")
    if type_filter:
        query = query.filter_by(type=type_filter)

    # filtro por período
    start = request.args.get("start")
    end = request.args.get("end")
    if start:
        query = query.filter(Movement.created_at >= start)
    if end:
        query = query.filter(Movement.created_at <= end)

    movements = query.order_by(Movement.created_at.desc()).all()
    users = User.query.all()  # para popular o select

    return render_template("movimentacoes.html", movements=movements, users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = request.form["username"]  # pode ser username ou email
        password = request.form["password"]

        # tenta buscar por username ou email
        user = User.query.filter(
            (User.username == login_input) | (User.email == login_input)
        ).first()

        if user and user.check_password(password):
            login_user(user, remember=True)  # cria sessão permanente
            session.permanent = True         # ativa controle de expiração
            return redirect(url_for("index"))
        else:
            flash("Usuário/e-mail ou senha inválidos", "error")

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

    users = User.query.all()
    return render_template("create_user.html", users=users)

    users = User.query.all()
    return render_template("create_user.html", users=users)

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@admin_required   # <<< Apenas admin pode editar outros usuários
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        # Atualiza os campos
        user.email = request.form["email"]
        user.role = request.form["role"]

        # Se o admin quiser alterar a senha
        if request.form.get("password"):
            user.set_password(request.form["password"])

        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("create_user"))  # volta para lista de usuários

    return render_template("edit_user.html", user=user)

@app.route("/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    # Impede que o admin exclua a si mesmo
    if user.id == current_user.id:
        flash("Você não pode excluir a si mesmo!", "error")
        return redirect(url_for("create_user"))

    db.session.delete(user)
    db.session.commit()
    flash("Usuário excluído com sucesso!", "success")
    return redirect(url_for("create_user"))

@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_password_hash(str(user.id) + str(datetime.now()))
            # Aqui você salvaria o token em uma tabela ou cache
            msg = Message("Reset de senha - Sistema de Correios",
                          sender="seuemail@dominio.com",
                          recipients=[user.email])
            msg.body = f"Olá, clique no link para resetar sua senha: http://localhost:5000/reset_password/{user.id}"
            mail.send(msg)
            flash("E-mail de reset enviado!", "success")
        else:
            flash("E-mail não encontrado!", "error")
    return render_template("reset_password_request.html")

@app.route("/reset_password/<int:user_id>", methods=["GET", "POST"])
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        new_password = request.form["new_password"]
        user.set_password(new_password)
        db.session.commit()
        flash("Senha redefinida com sucesso!", "success")
        return redirect(url_for("login"))
    return render_template("reset_password.html", user=user)


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

# ---------------------
# Inicialização
# ---------------------
if __name__ == "__main__":
    app.run(debug=True)
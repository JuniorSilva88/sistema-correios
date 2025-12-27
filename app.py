from flask import Flask, render_template, request, redirect, url_for, Response, abort, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from flask_migrate import Migrate
from flask_mail import Mail, Message
import uuid 
import os 
import barcode 
from barcode.writer import ImageWriter
from PIL import Image # opcional, mas confirma Pillow instalado

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://junior:senha123@localhost/correios'
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

def gerar_barcode(protocolo):
    # Caminho absoluto para a pasta static/barcodes 
    pasta = os.path.join(app.root_path, "static", "barcodes")
    os.makedirs(pasta, exist_ok=True)

    # NÃO coloque .png aqui, o writer já adiciona
    filename = os.path.join(pasta, protocolo)

    # Gera o código de barras em PNG
    code128 = barcode.get("code128", protocolo, writer=ImageWriter())
    code128.save(filename)

    print(f"✅ Código de barras gerado: {filename}.png")

    # Retorna caminho relativo correto para usar no template
    return f"barcodes/{protocolo}.png"

# ---------------------------
# Modelos
# ---------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # "user" ou "admin"
    status = db.Column(db.String(20), default="pendente")  # <<< NOVO: pendente, ativo, inativo

    def set_password(self, password):
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
        # Validação: só permite saída se o item tiver destinatário registrado
        if not item.recipient:
            flash("Item sem destinatário registrado na entrada.", "error")
            return redirect(url_for("exit_item", protocol=protocol))

        # Registro da saída
        item.status = "Finalizado"
        item.closed = datetime.now()

        move = Movement(
            protocol=protocol,
            type="Saída",
            location=request.form["location"],
            note=request.form.get("note", ""),
            created_at=datetime.now(),
            user=current_user.username
        )
        db.session.add(move)
        db.session.commit()

        flash("Saída registrada com sucesso!", "success")
        return redirect(url_for("index"))

    return render_template("exit_item.html", item=item)

@app.route("/create_admin")
def create_admin():
    existing_admin = User.query.filter_by(username="admin").first()
    if existing_admin:
        return "⚠️ Usuário admin já existe!", 400

    admin = User(
        username="admin",
        email="admin@dominio.com",
        role="admin",
        status="ativo"  # ✅ garante acesso
    )
    admin.set_password("1234")
    db.session.add(admin)
    db.session.commit()

    return "✅ Usuário admin criado com sucesso! Login: admin / Senha: 1234"


@app.route("/movimentacoes")
@login_required
def movimentacoes():
    # Base: começa com Movement e faz join com Item para permitir filtros por campos do Item
    query = db.session.query(Movement).join(Item, Movement.protocol == Item.protocol)

    # Filtros existentes (mantidos)
    user_filter = request.args.get("usuario")
    type_filter = request.args.get("tipo")
    start = request.args.get("data_inicio")
    end = request.args.get("data_fim")

    # NOVO: termo de busca livre (protocolo, remetente, destinatário, descrição)
    q = request.args.get("q")

    movements = []  # começa vazio para só exibir após ação (FILTRAR ou busca)

    # Só busca se houver pelo menos um filtro aplicado ou termo de busca
    if user_filter or type_filter or start or end or q:
        # ===== Filtros existentes =====
        if user_filter:
            query = query.filter(Movement.user == user_filter)

        if type_filter:
            # Aceita 'entrada'/'saida' do select e compara com valores de Movement.type
            query = query.filter(Movement.type.ilike(type_filter))

        if start:
            # Converte start para datetime para comparação correta
            try:
                start_dt = datetime.strptime(start, "%Y-%m-%d")
                query = query.filter(Movement.created_at >= start_dt)
            except ValueError:
                pass  # ignora formato inválido

        if end:
            # Inclui fim do dia para capturar registros do dia inteiro
            try:
                end_dt = datetime.strptime(end, "%Y-%m-%d")
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Movement.created_at <= end_dt)
            except ValueError:
                pass  # ignora formato inválido

        # ===== NOVO: Busca avançada =====
        if q:
            like_q = f"%{q}%"
            query = query.filter(
                (Item.protocol.ilike(like_q)) |
                (Item.sender.ilike(like_q)) |
                (Item.recipient.ilike(like_q)) |
                (Item.description.ilike(like_q))
            )

        # Ordenação por mais recente
        movements = query.order_by(Movement.created_at.desc()).all()

        # Enriquecimento de dados para o template (inclui Destinatário)
        for m in movements:
            item = Item.query.filter_by(protocol=m.protocol).first()
            m.description = item.description if item else ""
            m.destinatario = item.recipient if item else ""  # NOVO: destinatário para a coluna
            m.status = item.status if item else ""
            m.usuario = m.user
            m.tipo = m.type
            m.data = m.created_at

    # Lista de usuários para o select de filtro
    users = [u[0] for u in db.session.query(Movement.user).distinct().all()]

    return render_template("movimentacoes.html", movements=movements, users=users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = request.form["username"]  # pode ser username ou email
        password = request.form["password"]

        user = User.query.filter(
            (User.username == login_input) | (User.email == login_input)
        ).first()

        if user and user.check_password(password):
            if user.status != "ativo":   # <<< BLOQUEIO
                flash("⚠️ Usuário ainda não aprovado pelo administrador.", "error")
                return redirect(url_for("login"))

            login_user(user, remember=True)
            session.permanent = True
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Usuário ou e-mail já existe!", "error")
            return redirect(url_for("register"))

        user = User(username=username, email=email, role="user", status="pendente")  # <<< pendente
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Cadastro realizado! Aguarde aprovação do administrador.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/validate_users", methods=["GET", "POST"])
@admin_required
def validate_users():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        action = request.form.get("action")  # "aprovar" ou "rejeitar"
        user = User.query.get_or_404(user_id)

        if action == "aprovar":
            user.status = "ativo"
        elif action == "rejeitar":
            user.status = "inativo"

        db.session.commit()
        flash("Status do usuário atualizado!", "success")
        return redirect(url_for("validate_users"))

    users = User.query.all()
    return render_template("validate_users.html", users=users)


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

        items = query.all()
        result = []

        for item in items:
            last_move = Movement.query.filter_by(protocol=item.protocol)\
                                      .order_by(Movement.created_at.desc())\
                                      .first()

            # Verifica se a movimentação está dentro do intervalo de datas
            if start_date and end_date and last_move and last_move.created_at:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                end_dt = end_dt.replace(hour=23, minute=59, second=59)

                if not (start_dt <= last_move.created_at <= end_dt):
                    continue  # pula esse item

            item.usuario = last_move.user if last_move else "-"
            item.tipo = last_move.type if last_move else "-"
            item.data = last_move.created_at if last_move else None
            item.destinatario = item.recipient
            result.append(item)

        filtered = result

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

    items = query.all()
    lines = ["Protocolo,Descrição,Status,Remetente,Destinatário,Usuário,Tipo,Data,Local,Nota"]

    for item in items:
        # Buscar todas as movimentações do item
        moves = Movement.query.filter_by(protocol=item.protocol).order_by(Movement.created_at.asc()).all()

        for move in moves:
            # Filtro por data usando movimentação
            if start_date and end_date and move.created_at:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                end_dt = end_dt.replace(hour=23, minute=59, second=59)

                if not (start_dt <= move.created_at <= end_dt):
                    continue  # pula movimentação fora do intervalo

            usuario = move.user if move.user else ""
            tipo = move.type if move.type else ""
            data_mov = move.created_at.strftime("%Y-%m-%d %H:%M:%S") if move.created_at else ""
            local = move.location if move.location else ""
            nota = move.note if move.note else ""

            lines.append(f"{item.protocol},{item.description},{item.status},{item.sender},{item.recipient},{usuario},{tipo},{data_mov},{local},{nota}")

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

@app.route("/item_history/<protocol>")
@login_required
def item_history(protocol):
    item = Item.query.filter_by(protocol=protocol).first_or_404()
    movements = Movement.query.filter_by(protocol=protocol)\
                              .order_by(Movement.created_at.desc()).all()
    return render_template("item_history.html", item=item, movements=movements)


@app.route("/etiqueta/<int:item_id>")
@login_required
def etiqueta(item_id):
    item = Item.query.get_or_404(item_id)
    barcode_path = gerar_barcode(item.protocol)

    # captura filtros da query string
    filters = request.args.to_dict()

    return render_template("etiqueta.html", item=item, barcode_path=barcode_path, filters=filters)


# ---------------------
# Inicialização
# ---------------------
if __name__ == "__main__":
    app.run(debug=True)
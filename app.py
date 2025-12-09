import os
import random
import string
from datetime import datetime
from enum import Enum

from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'troque-esta-chave'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mailtrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ MODELOS ------------------
class ItemType(Enum):
    document = "Documento"
    package = "Pacote"

class MoveType(Enum):
    entry = "Entrada"
    exit = "Saída"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120))
    password_hash = db.Column(db.String(256))

class Party(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(50), unique=True, nullable=False)
    item_type = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(255))
    sender_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    current_status = db.Column(db.String(50), default="Recebido")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime, nullable=True)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    move_type = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(120))
    note = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ------------------ FUNÇÕES ------------------
def generate_protocol():
    date_part = datetime.utcnow().strftime("%Y%m%d")
    rand_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"PRT-{date_part}-{rand_part}"

def get_party_name(pid):
    p = Party.query.get(pid)
    return p.name if p else "-"

def fmt_dt(dt):
    return dt.strftime("%d/%m/%Y %H:%M") if dt else "-"

# ------------------ ROTAS ------------------
@app.route('/init')
def init():
    db.create_all()
    if not User.query.filter_by(email='admin@local').first():
        admin = User(email='admin@local', name='Admin',
                     password_hash=generate_password_hash('admin123'))
        db.session.add(admin)
    db.session.commit()
    return "Banco inicializado com sucesso!"

@app.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template("index.html", items=items, get_party_name=get_party_name, fmt_dt=fmt_dt)

@app.route('/new_item', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        sender_name = request.form['sender']
        recipient_name = request.form['recipient']
        description = request.form['description']
        item_type = request.form['item_type']

        sender = Party.query.filter_by(name=sender_name).first() or Party(name=sender_name)
        recipient = Party.query.filter_by(name=recipient_name).first() or Party(name=recipient_name)
        db.session.add(sender)
        db.session.add(recipient)
        db.session.commit()

        protocol = generate_protocol()
        item = Item(protocol=protocol, item_type=item_type,
                    description=description, sender_id=sender.id,
                    recipient_id=recipient.id, current_status="Recebido")
        db.session.add(item)
        db.session.commit()

        admin = User.query.filter_by(email="admin@local").first()
        move = Movement(item_id=item.id, move_type=MoveType.entry.value,
                        location="Recepção", created_by=admin.id)
        db.session.add(move)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template("new_item.html")

@app.route('/movements/<protocol>')
def movements(protocol):
    item = Item.query.filter_by(protocol=protocol).first_or_404()
    moves = Movement.query.filter_by(item_id=item.id).all()
    return render_template("movements.html", item=item, moves=moves, fmt_dt=fmt_dt)

@app.route('/exit/<protocol>', methods=['GET', 'POST'])
def exit_item(protocol):
    item = Item.query.filter_by(protocol=protocol).first_or_404()
    if request.method == 'POST':
        item.current_status = "Entregue"
        item.closed_at = datetime.utcnow()
        admin = User.query.filter_by(email="admin@local").first()
        move_exit = Movement(item_id=item.id, move_type=MoveType.exit.value,
                             location=request.form['location'], note=request.form['note'],
                             created_by=admin.id)
        db.session.add(move_exit)
        db.session.commit()
        return redirect(url_for('movements', protocol=item.protocol))
    return render_template("exit_item.html", item=item)

@app.route('/report', methods=['GET', 'POST'])
def report():
    sections = Party.query.all()
    items = []
    if request.method == 'POST':
        items = Item.query.all()
    return render_template("report.html", items=items, sections=sections, fmt_dt=fmt_dt, get_party_name=get_party_name)

if __name__ == "__main__":
    app.run()

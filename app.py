from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///correios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos
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


@app.route("/")
def index():
    items = Item.query.all()
    return render_template("dashboard.html", items=items)


@app.route("/new_item", methods=["GET", "POST"])
def new_item():
    if request.method == "POST":
        protocol = f"2025-{Item.query.count()+1:04d}"

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
def movements(protocol):
    item = Item.query.filter_by(protocol=protocol).first()
    item_moves = Movement.query.filter_by(protocol=protocol).all()
    return render_template("movements.html", item=item, moves=item_moves)


@app.route("/movimentacoes")
def movimentacoes():
    movements = Movement.query.all()
    return render_template("movimentacoes.html", movements=movements)


@app.route("/exit_item/<protocol>", methods=["GET", "POST"])
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


@app.route("/report", methods=["GET", "POST"])
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

            query = query.filter(
                (Item.closed == None) | ((Item.closed >= start_dt) & (Item.closed <= end_dt))
            )

        filtered = query.all()

    recipients = [r[0] for r in db.session.query(Item.recipient).distinct().all()]
    recipients.insert(0, "Todos")

    return render_template("report.html", items=filtered, sections=recipients)


@app.route("/report_csv", methods=["POST"])
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
        query = query.filter(
            (Item.closed == None) | ((Item.closed >= start_dt) & (Item.closed <= end_dt))
        )

    items = query.all()

    lines = ["Protocolo,Descrição,Status,Remetente,Destinatário,Fechamento"]
    for item in items:
        closed = item.closed.strftime("%d/%m/%Y %H:%M:%S") if item.closed else ""
        lines.append(f"{item.protocol},{item.description},{item.status},{item.sender},{item.recipient},{closed}")

    csv_data = "\n".join(lines)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=relatorio.csv"}
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

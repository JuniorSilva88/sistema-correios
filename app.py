from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulação de banco em memória
items = []
moves = []

@app.route("/")
def index():
    return render_template("dashboard.html", items=items)

@app.route("/new_item", methods=["GET", "POST"])
def new_item():
    if request.method == "POST":
        protocol = f"2025-{len(items)+1:04d}"
        item = {
            "protocol": protocol,
            "sender": request.form["sender"],
            "recipient": request.form["recipient"],
            "description": request.form["description"],
            "status": "Em trânsito",
            "closed": None
        }
        items.append(item)
        return redirect(url_for("index"))
    return render_template("new_item.html")

@app.route("/movements/<protocol>")
def movements(protocol):
    item = next((i for i in items if i["protocol"] == protocol), None)
    item_moves = [m for m in moves if m["protocol"] == protocol]
    return render_template("movements.html", item=item, moves=item_moves)

@app.route("/exit_item/<protocol>", methods=["GET", "POST"])
def exit_item(protocol):
    item = next((i for i in items if i["protocol"] == protocol), None)
    if request.method == "POST" and item:
        move = {
            "protocol": protocol,
            "type": "Saída",
            "location": request.form["location"],
            "note": request.form["note"],
            "created_at": "2025-12-11"
        }
        moves.append(move)
        item["status"] = "Finalizado"
        item["closed"] = "2025-12-11"
        return redirect(url_for("movements", protocol=protocol))
    return render_template("exit_item.html", item=item)

@app.route("/report", methods=["GET", "POST"])
def report():
    filtered = items
    if request.method == "POST":
        # Aqui você pode aplicar filtros de data/section
        pass
    return render_template("report.html", items=filtered, sections=["Seção 1", "Seção 2", "Seção 3"])

if __name__ == "__main__":
    app.run(debug=True)

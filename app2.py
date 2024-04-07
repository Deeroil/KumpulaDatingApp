from flask import Flask
from flask import render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    # return "Heipsun!! :3"
    return render_template("index.html")


@app.route("/wau")
def page1():
    return "JEEEE"


@app.route("/wow")
def page2():
    return "JOOO"


@app.route("/page/<int:id>")
def page(id):
    return "Tämä on sivu " + str(id)


@app.route("/page/<string:name>")
def pageName(name):
    return "Heips " + name + "!"


@app.route("/apina")
def apina():
    words = ["apina", "banaani", "cembalo"]
    return render_template("apina.html", message="Tervetuloa!", items=words)


@app.route("/kroko")
def kroko():
    return render_template("kuva.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", name=request.form["name"])


@app.route("/order")
def order():
    return render_template("order.html")


@app.route("/pizzaresult", methods=["POST"])
def pizzaresult():
    pizza = request.form["pizza"]
    extras = request.form.getlist("extra")
    message = request.form["message"]
    return render_template(
        "pizzaresult.html", pizza=pizza, extras=extras, message=message
    )

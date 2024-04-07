from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)


@app.route("/")
def index():
    # result = db.session.execute("SELECT content FROM messages")
    result = db.session.execute(text("SELECT content FROM messages"))

    messages = result.fetchall()
    return render_template("dbindex.html", count=len(messages), messages=messages)


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = text("INSERT INTO messages (content) VALUES (:content)")
    # db.session.execute(sql, {"content":content})
    db.session.execute(sql, {"content": content})

    db.session.commit()
    return redirect("/")

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
    result = db.session.execute(text("SELECT name, studyfield_id, bio FROM users"))
    users = result.fetchall()
    return render_template("dbindex.html", count=len(users), users=users)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    field = request.form["field"]
    bio = request.form["bio"]

    # haetaan id ensin
    result = db.session.execute(text("SELECT id FROM studyfields WHERE field=:field;"), {"field": field})
    id = result.fetchone()
    id = id[0]

    sql = text("INSERT INTO users (name, studyfield_id, bio) VALUES (:name, :studyfield_id, :bio)")

    db.session.execute(sql, {"name": name, "studyfield_id": id, "bio": bio})

    db.session.commit()
    return redirect("/")
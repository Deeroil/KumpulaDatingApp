from sqlalchemy.sql import text
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")

db = SQLAlchemy(app)


### TODO:
#       - like function/checkbox tjsp. form :D
#       - sit kans cancel option
#       - kirjautumistoiminto           !!!
#       - profiilin muokkaaminen
#       - handle tyhjät/jne/validoi/jne form jne
#       - hakuominaisuutta?


@app.route("/")
def index():
    return render_template("index.html")


# TODO: älä näytä omaa profiilia listauksessa
@app.route("/profiles")
def profiles():
    # result = db.session.execute(text("SELECT name, studyfield_id, bio FROM users"))
    command = "SELECT name, studyfields.field, bio FROM users LEFT JOIN studyfields ON studyfields.id = users.studyfield_id"
    # command = "SELECT username, name, studyfields.field, bio FROM users LEFT JOIN studyfields ON studyfields.id = users.studyfield_id WHERE username !=:username"

    # result = db.session.execute(text(command), {"username": session.username})
    result = db.session.execute(text(command))
    users = result.fetchall()
    return render_template("profiles.html", count=len(users), users=users)


@app.route("/new")
def new():
    return render_template("new.html")


def get_field_id(fieldname):
    result = db.session.execute(
        text("SELECT id FROM studyfields WHERE field=:field;"), {"field": fieldname}
    )
    return result.fetchone()[0]


@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    field = request.form["field"]
    bio = request.form["bio"]

    # haetaan id ensin
    id = get_field_id(field)

    sql = text(
        "INSERT INTO users (name, studyfield_id, bio) VALUES (:name, :studyfield_id, :bio)"
    )

    db.session.execute(sql, {"name": name, "studyfield_id": id, "bio": bio})

    db.session.commit()
    return redirect("/profiles")


@app.route("/sendregister", methods=["POST"])
def sendregister():
    # TODO:
    # - käyttäjänimen validointi (pituus jne)
    # - salasanan valdointi
    # - errors
    # - kamalaa joutua täyttää uudestaan jos ei saa
    #           luotua, mutta tehdään nyt näin

    username = request.form["username"]
    passw = request.form["passw"]
    name = request.form["name"]
    field = request.form["field"]
    bio = request.form["bio"]

    # haetaan usernamella ensin
    result = db.session.execute(
        text("SELECT username FROM users WHERE username=:username;"),
        {"username": username},
    )
    user = result.fetchone()

    if user:
        # TODO: Error1!
        print("error: user exists")
    else:
        passw_hashed = generate_password_hash(passw)
        id = get_field_id(field)

        sql = text(
            "INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES (:username, :passw, :name, :studyfield_id, :bio)"
        )

        db.session.execute(
            sql,
            {
                "username": username,
                "passw": passw_hashed,
                "name": name,
                "studyfield_id": id,
                "bio": bio,
            },
        )
        db.session.commit()
    return redirect("/new")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    sql = text("SELECT id, passw FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        # TODO: invalid username
        print("Error: invalid username")
    else:
        hash_value = user.passw
        if check_password_hash(hash_value, password):
            # TODO: correct username and password
            print("Jee läpi meni")
        else:
            # TODO: invalid password
            print("Error: väärä salasana")

    session["username"] = username
    return redirect("/profiles")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

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
    command = "SELECT username, name, studyfields.field, bio FROM users LEFT JOIN studyfields ON studyfields.id = users.studyfield_id"
    result = db.session.execute(text(command))
    users = result.fetchall()
    return render_template("profiles.html", count=len(users), users=users)


@app.route("/sendlikes", methods=["POST"])
def sendlikes():

    command = text("SELECT username, id FROM users")
    result = db.session.execute(command)
    users = result.fetchall()

    liked = []
    for user in users:
        u = request.form.get(user.username)
        if u:
            liked.append(user.id)

    # print("USERNAMES LIKED:", liked)

    username = session["username"]
    command = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(command, {"username": username})
    user_id = result.fetchone()[0]

    if len(liked) > 0:
        for likee_id in liked:
            command = text(
                "INSERT INTO likes (liker_id, likee_id) VALUES (:liker_id, :likee_id)"
            )
            result = db.session.execute(
                command, {"liker_id": user_id, "likee_id": likee_id}
            )

    db.session.commit()  # tää tänne vai tonne sisälle?

    return redirect("/profiles")


@app.route("/new")
def new():
    return render_template("new.html")


def get_field_id(fieldname):
    result = db.session.execute(
        text("SELECT id FROM studyfields WHERE field=:field"), {"field": fieldname}
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
        text("SELECT username FROM users WHERE username=:username"),
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
    return redirect("/")


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
            session["username"] = username
            return redirect("/profiles")
        else:
            # TODO: invalid password
            print("Error: väärä salasana")
            return redirect("/")
    # TODO: osoita että oli virhe?
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

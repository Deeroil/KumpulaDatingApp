
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sql_functions as fun
from app import app
from db import db


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profiles")
def profiles():
    users = fun.find_userdata()
    return render_template("profiles.html", count=len(users), users=users)


@app.route("/sendlikes", methods=["POST"])
def sendlikes():
    users = fun.find_username_id()
    liked = []
    for user in users:
        u = request.form.get(user.username)
        if u:
            liked.append(user.id)

    username = session["username"]
    user_id = fun.find_session_id(username)

    if len(liked) > 0:
        for likee_id in liked:
            fun.insert_like(user_id, likee_id)

    db.session.commit()  # tää tänne insert_like:n sisälle?

    return redirect("/profiles")


@app.route("/new")
def new():
    return render_template("new.html")


# TODO: edit this to be edit profile
@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    field = request.form["field"]
    bio = request.form["bio"]

    # haetaan id ensin
    studyfield_id = fun.get_field_id(field)

    fun.create_new_user(name, studyfield_id, bio)
    return redirect("/profiles")


@app.route("/sendregister", methods=["POST"])
def sendregister():
    # TODO:
    # - käyttäjänimen validointi (pituus jne)
    # -radio validation?
    # - salasanan valdointi
    # - errors
    # - kamalaa joutua täyttää uudestaan jos ei saa
    #           luotua, mutta tehdään nyt näin

    username = request.form["username"]
    passw = request.form["passw"]
    name = request.form["name"]
    field = request.form["field"]
    bio = request.form["bio"]

    print("FIELD", field)
    # haetaan usernamella ensin
    user = fun.find_username(username)

    if user:
        print("error: user exists")
        return render_template("error.html", message="Käyttäjätunnus on jo olemassa")
    else:
        passw_hashed = generate_password_hash(passw)
        field_id = fun.get_field_id(field)
        fun.create_user(username, passw_hashed, name, field_id, bio)
        db.session.commit()

    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = fun.find_id_passw(username)

    if not user:
        print("Error: invalid username")
        return render_template("error.html", message="Käyttäjätunnusta ei olemassa")
    else:
        hash_value = user.passw
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/profiles")
        else:
            print("Error: väärä salasana")
            return render_template("error.html", message="Väärä salasana")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

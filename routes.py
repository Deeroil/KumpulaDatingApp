from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sql_functions as fun
from app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profiles")
def profiles():
    users = fun.find_userdata()

    username = session["username"]
    user_id = fun.find_session_id(username)
    matches = fun.find_matches(user_id)

    return render_template("profiles.html", count=len(users), users=users, matches=matches)


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

    if not username or not passw or not name or not field:
        return render_template("error.html", message="Tietoja puuttuu")

    # TODO: näinkö?
    if not 2 < len(username) < 26:
        return render_template(
            "error.html", message="Käyttäjänimen tulee olla 3-25 merkkiä pitkä"
        )

    if not 11 < len(passw) < 36:
        return render_template(
            "error.html", message="Salasanan tulee olla 12-35 merkkiä pitkä"
        )

    if not 1 < len(name) < 16:
        return render_template(
            "error.html", message="Nimen tulee olla 2-15 merkkiä pitkä"
        )

    if not 2 < len(name) < 201:
        return render_template(
            "error.html", message="Profiilitekstin tulee olla 3-200 merkkiä pitkä"
        )

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

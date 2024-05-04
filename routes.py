from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
import sql_functions as fun
import secrets
from app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profiles")
def profiles():
    if "username" in session:
        username = session["username"]
        users = fun.find_userdata_no_curr(username)
        user_id = fun.find_session_id(username)
        matches = fun.find_match_usernames(user_id)
        matches = tuplelist_helper(matches)
        print("matches now:", matches)

        likes = fun.get_liked_usernames(user_id)
        likes = tuplelist_helper(likes)

        return render_template(
            "profiles.html", count=len(users), users=users, likes=likes, matches=matches
        )
    else:
        return render_template("profiles.html")


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


@app.route("/matches")
def matches():
    if "username" in session:
        username = session["username"]
        user_id = fun.find_session_id(username)
        matchlist = fun.find_match_profiles(user_id)

        return render_template("matches.html", count=len(matchlist), matches=matchlist)
    else:
        return render_template("matches.html")


def tuplelist_helper(tuplelist):
    """make a set out of tuple list"""
    items = set()
    for i in tuplelist:
        # print(i[0])
        items.add(i[0])
    return items


@app.route("/edit")
def edit():
    if "username" in session:
        username = session["username"]
        user = fun.find_name_bio(username)

        orientations = fun.get_user_orientations(username)
        orientations = tuplelist_helper(orientations)
        print(orientations)

        return render_template("edit.html", user=user, ori=orientations)
    else:
        return render_template("edit.html")


@app.route("/editprofile", methods=["POST"])
def editprofile():
    name = request.form["name"]
    bio = request.form["bio"]

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    user_id = fun.find_session_id(session["username"])
    fun.edit_user(user_id, name, bio)
    return redirect("/profiles")


@app.route("/editorientations", methods=["POST"])
def editorientations():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    orientations = fun.get_orientations()
    username = session["username"]
    user_id = fun.find_session_id(username)
    user_orientations = fun.get_user_orientations(username)  # TODO: ???
    user_orientations = tuplelist_helper(user_orientations)
    # print("oris", orientations)
    # print("userori", user_orientations)

    add = []
    remove = []
    for ori in orientations:
        # print("ori[0]", ori[0])
        u = request.form.get(ori[0])
        # print("u", u)
        if u and ori[0] not in user_orientations:
            add.append(ori[0])

        if not u and ori[0] in user_orientations:
            remove.append(ori[0])

    # print("Add, ", add)
    # print("Remouv", remove)

    for ori in add:
        orientation_id = fun.get_orientation_id(ori)
        fun.add_orientation(user_id, orientation_id)

    for ori in remove:
        orientation_id = fun.get_orientation_id(ori)
        fun.delete_orientation(user_id, orientation_id)

    return redirect("/profiles")


# TODO: check radiobox does it work without-- no.
@app.route("/sendregister", methods=["POST"])
def sendregister():
    # TODO:
    # -radio validation?
    # - salasanan valdointi
    # - kamalaa joutua täyttää uudestaan jos ei saa
    #           luotua, mutta tehdään nyt näin

    username = request.form["username"]
    passw = request.form["passw"]
    name = request.form["name"]
    field = request.form["field"]
    bio = request.form["bio"]

    if not username or not passw or not name or not field:
        return render_template("error.html", message="Missing information")

    # TODO: näinkö?
    if not 2 < len(username) < 26:
        return render_template(
            "error.html", message="Username should be 3-25 characters long"
        )

    if not 11 < len(passw) < 36:
        return render_template(
            "error.html", message="Password should be 12-35 characters long"
        )

    if not 1 < len(name) < 16:
        return render_template(
            "error.html", message="Name should be 2-15 characters long"
        )

    if not 2 < len(name) < 201:
        return render_template(
            "error.html", message="Profile text should be 3-200 characters long"
        )

    print("FIELD", field)
    # haetaan usernamella ensin
    user = fun.find_username(username)

    if user:
        print("error: user exists")
        return render_template("error.html", message="Username already exists")
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
        return render_template("error.html", message="Username doesn't exist")
    else:
        hash_value = user.passw
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/profiles")
        else:
            print("Error: wrong password")
            return render_template("error.html", message="Wrong password")


@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

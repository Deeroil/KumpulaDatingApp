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
        # print("matches now:", matches)

        likes = fun.get_liked_usernames(user_id)
        likes = tuplelist_helper(likes)
        # print("usersss,", users)

        userori = {}
        for u in users:
            ori = fun.get_user_orientations(u.username)
            ori = tuplelist_helper(ori)
            userori[u.username] = ori

        print("userori", userori)
        return render_template(
            "profiles.html",
            count=len(users),
            users=users,
            likes=likes,
            matches=matches,
            orientations=userori,
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

        userori = {}
        for u in matchlist:
            ori = fun.get_user_orientations(u.username)
            ori = tuplelist_helper(ori)
            userori[u.username] = ori

        return render_template(
            "matches.html",
            count=len(matchlist),
            matches=matchlist,
            orientations=userori,
        )
    else:
        return render_template("matches.html")


def tuplelist_helper(tuplelist):
    """make a list out of tuple list"""

    items = []
    for i in tuplelist:
        if i[0] not in items:
            items.append(i[0])

    if len(items) > 0:
        return items
    return None


@app.route("/edit")
def edit():
    if "username" in session:
        username = session["username"]
        user = fun.find_name_bio(username)

        orientations = fun.get_user_orientations(username)
        orientations = tuplelist_helper(orientations)
        all_orientations = fun.get_orientations()
        all_orientations = tuplelist_helper(all_orientations)
        # print("all:", all_orientations)
        # print("users", orientations)

        return render_template(
            "edit.html", user=user, ori=orientations, all_orientations=all_orientations
        )
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
    orientations = tuplelist_helper(orientations)
    username = session["username"]
    user_id = fun.find_session_id(username)
    user_orientations = fun.get_user_orientations(username)
    user_orientations = tuplelist_helper(user_orientations)
    # print("oris", orientations)
    # print("userori", user_orientations)

    add = []
    remove = []
    if user_orientations:
        for ori in orientations:
            u = request.form.get(ori)
            # print("u", u)
            if u and ori not in user_orientations:
                add.append(ori)

            if not u and ori in user_orientations:
                remove.append(ori)
    else:
        print("no orientations")
        for ori in orientations:
            u = request.form.get(ori)
            if u:
                add.append(ori)

    for new in add:
        orientation_id = fun.get_orientation_id(new)
        fun.add_orientation(user_id, orientation_id)

    for deleted in remove:
        orientation_id = fun.get_orientation_id(deleted)
        fun.delete_orientation(user_id, orientation_id)

    return redirect("/profiles")


@app.route("/sendregister", methods=["POST"])
def sendregister():
    username = request.form["username"]
    passw = request.form["passw"]
    name = request.form["name"]
    field = request.form["field"]
    bio = request.form["bio"]

    if not username or not passw or not name or not field:
        return render_template("error.html", message="Missing information")

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

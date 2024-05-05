from flask import redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
import src.likes as likes
import src.users as users
import src.orientations as orientations
import src.studyfields as studyfields
import src.helper_func as helper
import secrets
from app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profiles")
def profiles():
    if "username" in session:
        username = session["username"]
        userdata = users.get_userdata_no_curr(username)
        user_id = users.get_username_id(username)
        matches = likes.get_match_usernames(username)
        # print("matches now:", matches)

        liked_list = likes.get_liked_usernames(user_id)
        # print("usersss,", users)

        userori = {}
        for u in userdata:
            ori = orientations.get_user_orientations(u.username)
            ori = helper.tuplelist_helper(ori)
            userori[u.username] = ori

        liked_list = helper.tuplelist_helper(liked_list)
        matches = helper.tuplelist_helper(matches)

        print("userori", userori)
        return render_template(
            "profiles.html",
            count=len(userdata),
            users=userdata,
            likes=liked_list,
            matches=matches,
            orientations=userori,
        )
    else:
        return render_template("profiles.html")


@app.route("/sendlikes", methods=["POST"])
def sendlikes():
    users_list = users.get_usernames_ids()
    liked = []
    for user in users_list:
        u = request.form.get(user.username)
        if u:
            liked.append(user.id)

    username = session["username"]
    user_id = users.get_username_id(username)

    if len(liked) > 0:
        for likee_id in liked:
            try:
                likes.insert_like(user_id, likee_id)
            except (UniqueViolation, IntegrityError):
                return render_template(
                    "error.html", message="Invalid request. Like already exists."
                )

    return redirect("/profiles")


@app.route("/matches")
def matches():
    if "username" in session:
        username = session["username"]
        matchlist = likes.get_match_profiles(username)

        userori = {}
        for u in matchlist:
            ori = orientations.get_user_orientations(u.username)
            ori = helper.tuplelist_helper(ori)
            userori[u.username] = ori

        return render_template(
            "matches.html",
            count=len(matchlist),
            matches=matchlist,
            orientations=userori,
        )
    else:
        return render_template("matches.html")


@app.route("/edit")
def edit():
    if "username" in session:
        username = session["username"]
        user = users.get_names_bios(username)

        orien_list = orientations.get_user_orientations(username)
        all_orientations = orientations.get_all_orientations()

        orien_list = helper.tuplelist_helper(orien_list)
        all_orientations = helper.tuplelist_helper(all_orientations)

        # print("all:", all_orientations)
        # print("users", orientations)

        return render_template(
            "edit.html", user=user, ori=orien_list, all_orientations=all_orientations
        )
    else:
        return render_template("edit.html")


@app.route("/editprofile", methods=["POST"])
def editprofile():
    name = request.form["name"]
    bio = request.form["bio"]

    if error := helper.validate_edit(name, bio):
        return error

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    username = session["username"]
    users.edit_user(username, name, bio)
    return redirect("/profiles")


@app.route("/editorientations", methods=["POST"])
def editorientations():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    username = session["username"]
    user_orientations = orientations.get_user_orientations(username)
    orien_list = orientations.get_all_orientations()

    user_orientations = helper.tuplelist_helper(user_orientations)
    orien_list = helper.tuplelist_helper(orien_list)
    # print("oris", orientations)
    # print("userori", user_orientations)

    add = []
    remove = []
    if user_orientations:
        for ori in orien_list:
            u = request.form.get(ori)
            # print("u", u)
            if u and ori not in user_orientations:
                add.append(ori)

            if not u and ori in user_orientations:
                remove.append(ori)
    else:
        print("no orientations")
        for ori in orien_list:
            u = request.form.get(ori)
            if u:
                add.append(ori)

    user_id = users.get_username_id(username)
    for new in add:
        orientation_id = orientations.get_orientation_id(new)
        try:
            orientations.insert_user_orientation(user_id, orientation_id)
        except (UniqueViolation, IntegrityError):
            return render_template(
                "error.html", message="Invalid request. Orientation already added."
            )

    for deleted in remove:
        orientation_id = orientations.get_orientation_id(deleted)
        orientations.delete_orientation(user_id, orientation_id)

    return redirect("/profiles")


@app.route("/sendregister", methods=["POST"])
def sendregister():
    username = request.form["username"]
    passw = request.form["passw"]
    name = request.form["name"]
    field = request.form["field"]
    bio = request.form["bio"]

    if error := helper.validate_register(username, passw, name, field, bio):
        return error

    user = users.check_username_exists(username)
    if user:
        print("error: user exists")
        return render_template("error.html", message="Username already exists")
    else:
        passw_hashed = generate_password_hash(passw)
        field_id = studyfields.get_field_id(field)
        users.create_user(username, passw_hashed, name, field_id, bio)

    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = users.get_ids_passws(username)

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

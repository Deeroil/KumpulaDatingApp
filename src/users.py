from src.db import db
from sqlalchemy.sql import text


# user functions

def create_user(username, passw_hashed, name, field_id, bio):
    sql = text(
        """INSERT INTO users (username, passw, name, studyfield_id, bio)
            VALUES (:username, :passw, :name, :studyfield_id, :bio)
        """
    )

    db.session.execute(
        sql,
        {
            "username": username,
            "passw": passw_hashed,
            "name": name,
            "studyfield_id": field_id,
            "bio": bio,
        },
    )
    db.session.commit()


def edit_user(username, name, bio):
    sql = text("UPDATE users SET name=:name, bio=:bio WHERE username=:username")
    db.session.execute(sql, {"name": name, "bio": bio, "username": username})
    db.session.commit()


def check_username_exists(username):
    result = db.session.execute(
        text("SELECT username FROM users WHERE username=:username"),
        {"username": username},
    )
    return result.fetchone()


def get_usernames_ids():
    command = text("SELECT username, id FROM users")
    result = db.session.execute(command)
    return result.fetchall()


def get_username_id(username):
    command = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(command, {"username": username})
    return result.fetchone()[0]


def get_ids_passws(username):
    sql = text("SELECT id, passw FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_names_bios(username):
    sql = text("SELECT name, bio FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_userdata():
    command = text(
        """SELECT username, name, studyfields.field, bio
            FROM users
            LEFT JOIN studyfields ON studyfields.id = users.studyfield_id
        """
    )
    result = db.session.execute(command)
    users = result.fetchall()
    return users


def get_userdata_no_curr(username):
    command = text(
        """SELECT username, name, studyfields.field, bio
            FROM users
            LEFT JOIN studyfields ON studyfields.id = users.studyfield_id
            WHERE username != :username
        """
    )
    result = db.session.execute(command, {"username": username})
    users = result.fetchall()
    return users

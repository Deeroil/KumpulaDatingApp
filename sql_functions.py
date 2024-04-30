from db import db
from sqlalchemy.sql import text


# user functions
def create_user(username, passw_hashed, name, field_id, bio):
    sql = text(
        """
            INSERT INTO users (username, passw, name, studyfield_id, bio)
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


def find_username(username):
    result = db.session.execute(
        text("SELECT username FROM users WHERE username=:username"),
        {"username": username},
    )
    return result.fetchone()


def find_username_id():
    command = text("SELECT username, id FROM users")
    result = db.session.execute(command)
    return result.fetchall()


def find_id_passw(username):
    sql = text("SELECT id, passw FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def find_session_id(username):
    command = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(command, {"username": username})
    return result.fetchone()[0]


def find_userdata():
    command = text(
        """SELECT username, name, studyfields.field, bio
            FROM users
            LEFT JOIN studyfields ON studyfields.id = users.studyfield_id
        """
    )
    result = db.session.execute(command)
    users = result.fetchall()
    return users


# edit this to edit user
def create_new_user(name, studyfield_id, bio):
    sql = text(
        "INSERT INTO users (name, studyfield_id, bio) VALUES (:name, :studyfield_id, :bio)"
    )

    db.session.execute(sql, {"name": name, "studyfield_id": studyfield_id, "bio": bio})
    db.session.commit()


# other functions
def insert_like(liker_id, likee_id):
    command = text(
        "INSERT INTO likes (liker_id, likee_id) VALUES (:liker_id, :likee_id)"
    )
    db.session.execute(command, {"liker_id": liker_id, "likee_id": likee_id})
    db.session.commit()


def get_field_id(fieldname):
    result = db.session.execute(
        text("SELECT id FROM studyfields WHERE field=:field"), {"field": fieldname}
    )
    return result.fetchone()[0]

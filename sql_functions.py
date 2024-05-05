from db import db
from sqlalchemy.sql import text

# TODO: rename näitä selkeämmiksi


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


def find_name_bio(username):
    sql = text("SELECT name, bio FROM users WHERE username=:username")
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


def find_userdata_no_curr(username):
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


def edit_user(user_id, name, bio):
    sql = text("UPDATE users SET name=:name, bio=:bio WHERE id=:user_id")
    db.session.execute(sql, {"name": name, "bio": bio, "user_id": user_id})
    db.session.commit()


# other functions
def insert_like(liker_id, likee_id):
    command = text(
        "INSERT INTO likes (liker_id, likee_id) VALUES (:liker_id, :likee_id)"
    )
    db.session.execute(command, {"liker_id": liker_id, "likee_id": likee_id})
    db.session.commit()


def get_liked_usernames(liker_id):
    command = text(
        """SELECT username
            FROM users
            LEFT JOIN likes ON likes.likee_id = users.id
            WHERE likes.liker_id=:liker_id
        """
    )
    result = db.session.execute(command, {"liker_id": liker_id})
    users = result.fetchall()
    return users


def find_match_profiles(user_id):
    command = text(
        """SELECT username, name, studyfields.field, bio FROM likes as A
            LEFT JOIN users ON users.id = A.likee_id
            LEFT JOIN studyfields ON studyfields.id = users.studyfield_id
            LEFT JOIN likes as B ON A.liker_id = B.likee_id
            WHERE A.likee_id =  B.liker_id
                    AND A.likee_id != B.likee_id
                    AND A.liker_id = :user_id
            GROUP BY studyfields.field, name, bio, username
        """
    )
    result = db.session.execute(command, {"user_id": user_id})
    return result.fetchall()


def find_match_usernames(user_id):
    command = text(
        """SELECT username FROM likes as A
            LEFT JOIN users ON users.id = A.likee_id
            LEFT JOIN likes as B ON A.liker_id = B.likee_id
            WHERE A.likee_id =  B.liker_id
                    AND A.likee_id != B.likee_id
                    AND A.liker_id = :user_id
            GROUP BY username
        """
    )
    result = db.session.execute(command, {"user_id": user_id})
    users = result.fetchall()
    print("WOO", users)
    return users


def get_field_id(fieldname):
    result = db.session.execute(
        text("SELECT id FROM studyfields WHERE field=:field"), {"field": fieldname}
    )
    return result.fetchone()[0]


def get_orientations():
    command = text(""" SELECT orientation FROM orientations""")
    result = db.session.execute(command)
    orientations = result.fetchall()
    print("ORIENTATIONS ALL", orientations)
    return orientations


def get_user_orientations(username):
    command = text(
        """SELECT orientation FROM user_orientations
            LEFT JOIN users ON users.id = user_orientations.user_id
            LEFT JOIN orientations ON orientations.id = user_orientations.orientation_id
            WHERE username = :username
        """
    )
    result = db.session.execute(command, {"username": username})
    orientations = result.fetchall()
    print("ORIENTATIONS", orientations)
    return orientations


def get_orientation_id(orientation):
    command = text("SELECT id FROM orientations WHERE orientation=:orientation")
    result = db.session.execute(command, {"orientation": orientation})
    return result.fetchone()[0]


def add_orientation(user_id, orientation_id):
    command = text(
        """INSERT INTO user_orientations (user_id, orientation_id)
            VALUES (:user_id, :orientation_id)
        """
    )

    db.session.execute(command, {"user_id": user_id, "orientation_id": orientation_id})
    db.session.commit()


def delete_orientation(user_id, orientation_id):
    command = text(
        """DELETE FROM user_orientations
            WHERE user_orientations.user_id=:user_id
            AND user_orientations.orientation_id=:orientation_id
        """
    )
    db.session.execute(command, {"user_id": user_id, "orientation_id": orientation_id})
    db.session.commit()

from db import db
from sqlalchemy.sql import text

# TODO: split into multiple files


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


def get_ids_passws(username):
    sql = text("SELECT id, passw FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_names_bios(username):
    sql = text("SELECT name, bio FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def get_username_id(username):
    command = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(command, {"username": username})
    return result.fetchone()[0]


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


def edit_user(username, name, bio):
    sql = text("UPDATE users SET name=:name, bio=:bio WHERE username=:username")
    db.session.execute(sql, {"name": name, "bio": bio, "username": username})
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


def get_match_profiles(username):
    command = text(
        """SELECT Y.username, Y.name, studyfields.field, Y.bio
            FROM likes as A
            LEFT JOIN users as X ON X.id = A.likee_id
            LEFT JOIN users as Y ON Y.id = A.liker_id
            LEFT JOIN studyfields ON studyfields.id = Y.studyfield_id
            LEFT JOIN likes as B ON A.liker_id = B.likee_id
            WHERE A.likee_id =  B.liker_id
                    AND A.likee_id != B.likee_id
                    AND X.username=:username
            GROUP BY studyfields.field, Y.name, Y.bio, Y.username
        """
    )
    result = db.session.execute(command, {"username": username})
    return result.fetchall()


def get_match_usernames(username):
    command = text(
        """SELECT Y.username FROM likes as A
            LEFT JOIN users as X ON X.id = A.likee_id
            LEFT JOIN users as Y ON Y.id = A.liker_id
            LEFT JOIN likes as B ON A.liker_id = B.likee_id
            WHERE A.likee_id =  B.liker_id
                    AND A.likee_id != B.likee_id
                    AND X.username=:username
            GROUP BY Y.username
        """
    )
    result = db.session.execute(command, {"username": username})
    users = result.fetchall()
    # print("Users", users)
    return users


def get_field_id(fieldname):
    result = db.session.execute(
        text("SELECT id FROM studyfields WHERE field=:field"), {"field": fieldname}
    )
    return result.fetchone()[0]


def get_all_orientations():
    command = text(""" SELECT orientation FROM orientations""")
    result = db.session.execute(command)
    orientations = result.fetchall()
    # print("ORIENTATIONS ALL", orientations)
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
    # print("USER'S ORIENTATIONS", orientations)
    return orientations


def get_orientation_id(orientation):
    command = text("SELECT id FROM orientations WHERE orientation=:orientation")
    result = db.session.execute(command, {"orientation": orientation})
    return result.fetchone()[0]


def insert_user_orientation(user_id, orientation_id):
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

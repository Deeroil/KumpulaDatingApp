from src.db import db
from sqlalchemy.sql import text


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
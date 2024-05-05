from src.db import db
from sqlalchemy.sql import text

# orientations functions

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

import sqlite3
import json
from datetime import datetime


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            select id, username
            from Users
            where username = ?
            and password = ?
        """,
            (user["username"], user["password"]),
        )

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {"valid": True, "token": user_from_db["id"]}
        else:
            response = {"valid": False}

        return json.dumps(response)


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """,
            (
                user["first_name"],
                user["last_name"],
                user["username"],
                user["email"],
                user["password"],
                user["bio"],
                datetime.now(),
            ),
        )

        id = db_cursor.lastrowid

        return json.dumps({"token": id, "valid": True})


def get_all_users():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT 
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username
        FROM Users as u
        """
        )

        users_from_db = db_cursor.fetchall()

        users = []

        for row in users_from_db:
            users.append(dict(row))

        sorted_results = sorted(users, key=lambda user: user["username"], reverse=False)

        serialized_results = json.dumps(sorted_results)
    return serialized_results


def get_user_detail(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT 
            u.id,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.profile_image_url,
            u.created_on,
            s.follower_id,
            s.id as sub_id
        FROM Users u
        JOIN Subscriptions s on s.author_id = u.id
        WHERE u.id = ?
        """,
            (pk,),
        )

        query_results = db_cursor.fetchall()

        if not query_results:
            return json.dumps({"error": "User not found"})

        user_data = {
            "id": query_results[0]["id"],
            "first_name": query_results[0]["first_name"],
            "last_name": query_results[0]["last_name"],
            "email": query_results[0]["email"],
            "bio": query_results[0]["bio"],
            "username": query_results[0]["username"],
            "profile_image_url": query_results[0]["profile_image_url"],
            "created_on": query_results[0]["created_on"],
            "followers": [
                (row["follower_id"], row["sub_id"])
                for row in query_results
                if row["follower_id"] is not None
            ],
        }
        serialized_result = json.dumps(user_data)
    return serialized_result

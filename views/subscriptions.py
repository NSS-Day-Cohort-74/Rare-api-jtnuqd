import sqlite3
import json


def create_subscription(data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Subscriptions
            (follower_id, author_id, created_on)
            VALUES (?, ?, ?)
            """,
            (
                data["follower_id"],
                data["author_id"],
                data["created_on"],
            ),
        )

    return True if db_cursor.rowcount > 0 else False


def delete_subscription(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Subscriptions WHERE id = ?
            """,
            (pk,),
        )

        return True if db_cursor.rowcount > 0 else False


def view_follower_subscriptions(follower_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                s.id,
                s.follower_id,
                s.author_id,
                s.created_on,
                u.first_name,
                u.last_name,
                p.title,
                p.category_id,
                c.label AS category_label
            FROM Subscriptions s
            JOIN Users u ON u.id = s.author_id
            JOIN Posts p ON p.user_id = s.author_id
            JOIN Categories c ON c.id = p.category_id
            WHERE s.follower_id = ?
            """,
            (follower_id,),
        )

        query_results = db_cursor.fetchall()

        subscriptions = []

        for row in query_results:
            subscriptions.append(dict(row))

        serialized_results = json.dumps(subscriptions)

    return serialized_results

import sqlite3


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

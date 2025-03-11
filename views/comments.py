import sqlite3
import json

def view_post_comments(post_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                c.id,
                c.post_id,
                c.author_id,
                c.content,
                u.first_name,
                u.last_name
            FROM Comments c
            JOIN Users u ON u.id = c.author_id
            WHERE c.post_id = ?
            """,
            (post_id,),
        )

        query_results = db_cursor.fetchall()

        comments = []

        for row in query_results:
            comments.append(dict(row))

        serialized_results = json.dumps(comments)

    return serialized_results
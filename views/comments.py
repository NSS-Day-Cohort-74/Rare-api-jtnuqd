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
                u.last_name,
                p.title
            FROM Comments c
            JOIN Users u ON u.id = c.author_id
            JOIN Posts p ON p.id = c.post_id
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

def create_comment(comment_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Comments
            (post_id, author_id, content)
            VALUES (?, ?, ?)
            """,
            (comment_data["post_id"], comment_data["author_id"], comment_data["content"],),
        )

    return True if db_cursor.rowcount > 0 else False

def delete_comment(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Comments WHERE id = ?
            """,
            (pk,),
        )

    return True if db_cursor.rowcount > 0 else False
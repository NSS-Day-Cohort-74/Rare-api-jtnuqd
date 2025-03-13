import sqlite3
import json

# NOTE: Not tested yet.


def view_all_post_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                pt.id,
                pt.post_id,
                pt.tag_id
            FROM posttags AS pt
            """
        )

        query_results = db_cursor.fetchall()

        post_tags = [dict(row) for row in query_results]

        sorted_results = sorted(post_tags, key=lambda tag: tag["tag_id"])

        return json.dumps(sorted_results)

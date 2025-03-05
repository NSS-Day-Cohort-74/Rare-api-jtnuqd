import sqlite3
import json

# NOTE: Tested

def view_all_tags():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                t.id,
                t.label
            FROM Tags AS t
            """
        )

        query_results = db_cursor.fetchall()

        tags = []

        for row in query_results:
            tags.append(dict(row))

        sorted_results = sorted(tags, key=lambda tag: tag["label"])
        serialized_results = json.dumps(sorted_results) if tags else []

    return serialized_results

def create_tag():
    pass
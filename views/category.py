import sqlite3
import json

# NOTE: Not tested yet.


def view_all_categories():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT 
                c.id,
                c.label
            FROM Categories AS c
            """
        )

        query_results = db_cursor.fetchall()

        categories = []

        for row in query_results:
            categories.append(dict(row))

        sorted_results = sorted(categories, key=lambda category: category["label"])
        serialized_results = json.dumps(sorted_results) if categories else []

    return serialized_results


def create_category(cat_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Categories
            (label)
            VALUES (?)
            """,
            (cat_data["label"],),
        )

    return True if db_cursor.rowcount > 0 else False

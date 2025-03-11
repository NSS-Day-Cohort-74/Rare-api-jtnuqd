import sqlite3
import json

# All posts should include post title, author name and category and date added.

def view_all_posts(user_id=None):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # // base SQL query
        query = """
        SELECT
            p.id, 
            p.title,
            p.publication_date, 
            p.category_id,
            p.user_id,
            c.label AS category_label,
            u.first_name,
            u.last_name
        FROM Posts AS p
        JOIN Categories c ON c.id = p.category_id
        JOIN Users u ON u.id = p.user_id
        """

        params = ()
        if user_id:  
            query += " WHERE p.user_id = ?"
            params = (user_id,)

        query += " ORDER BY p.publication_date DESC"  # // sorting by most recent first

        db_cursor.execute(query, params)
        query_results = db_cursor.fetchall()

        posts = [dict(row) for row in query_results]

        return json.dumps(posts)

# def view_all_posts():
#     with sqlite3.connect("./db.sqlite3") as conn:
#         conn.row_factory = sqlite3.Row
#         db_cursor = conn.cursor()

#         db_cursor.execute(
#             """
#         SELECT
#             p.id, 
#             p.title,
#             p.publication_date, 
#             p.category_id,
#             p.user_id,
#             c.label AS category_label,
#             u.first_name,
#             u.last_name
#         FROM Posts AS p
#         JOIN Categories c ON c.id = p.category_id
#         JOIN Users u ON u.id = p.user_id          
#         """
#         )
#         # Retrieve Results:
#         query_results = db_cursor.fetchall()

#         posts = []

#         for row in query_results:
#             posts.append(dict(row))

#         sorted_results = sorted(
#             posts, key=lambda post: post["publication_date"], reverse=True
#         )
#         serialized_results = json.dumps(sorted_results) if posts else {}
#     return serialized_results


# sorted_data = sorted(data, key=lambda x: x["name"])


def view_post_detail(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            p.id, 
            p.title,
            p.publication_date, 
            p.category_id,
            p.user_id,
            p.content,
            p.approved,
            c.label AS category_label,
            u.first_name,
            u.last_name
        FROM Posts AS p
        JOIN Categories c ON c.id = p.category_id
        JOIN Users u ON u.id = p.user_id
        WHERE p.id = ?          
        """,
            (pk,),
        )

        # Retrieve Results:
        query_result = db_cursor.fetchone()
        dictionary_version_of_object = dict(query_result) if query_result else {}

        serialized_result = json.dumps(dictionary_version_of_object)
    return serialized_result


def create_post(post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                post_data["user_id"],
                post_data["category_id"],
                post_data["title"],
                post_data["publication_date"],
                post_data["image_url"],
                post_data["content"],
                post_data["approved"],
            ),
        )

        new_post_id = db_cursor.lastrowid

    return new_post_id if new_post_id else None


def edit_post(pk, post_data):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            UPDATE 
                Posts
            SET
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?,
                user_id = ?
            WHERE
                id = ?
            """,
            (
                post_data["category_id"],
                post_data["title"],
                post_data["publication_date"],
                post_data["image_url"],
                post_data["content"],
                post_data["approved"],
                post_data["user_id"],
                pk,
            ),
        )
        rows_affected = db_cursor.rowcount
    return True if rows_affected > 0 else False


def delete_post(pk):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            DELETE FROM Posts WHERE id = ?
            """,
            (pk,),
        )
        number_of_rows_deleted = db_cursor.rowcount

    return True if number_of_rows_deleted > 0 else False


def get_current_user_posts(user_id):
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
            SELECT
                p.id, 
                p.title,
                p.publication_date,
                u.id,
                u.first_name,
                u.last_name
            FROM
            posts AS p
            JOIN Users u ON u.id = p.user_id
            WHERE
            p.user_id = ?
            """,
            (user_id,),
        )

        query_results = db_cursor.fetchall()

        posts = []

        for row in query_results:
            posts.append(dict(row))

        # sorted_results = sorted(posts, key=lambda tag: tag["label"])
        serialized_results = json.dumps(posts)

    return serialized_results

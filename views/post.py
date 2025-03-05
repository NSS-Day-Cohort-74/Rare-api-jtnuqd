import sqlite3
import json 


 # All posts should include post title, author name and category and date added.

def view_all_posts():
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
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
        """)
        # Retrieve Results:
        query_results = db_cursor.fetchall()

        posts = []
        
        for row in query_results:
            posts.append(dict(row))

        
        sorted_results = sorted(posts, key=lambda post: post['publication_date'], reverse = True)
        print(sorted_results)
        serialized_results = json.dumps(sorted_results) if posts else []
    return serialized_results

# sorted_data = sorted(data, key=lambda x: x["name"])
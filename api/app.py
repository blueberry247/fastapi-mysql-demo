import os
import time

import mysql.connector
from fastapi import FastAPI, HTTPException

# Create the FastAPI application object
app = FastAPI()

# === Read database configuration from environment variables ===
# These are set in docker-compose.yml for the "api" service.
# We also provide defaults so you can run it outside Docker if needed.
DB_HOST = os.getenv("DB_HOST", "db")           # "db" will be the MySQL service name
DB_PORT = int(os.getenv("DB_PORT", "3306"))    # Default MySQL port
DB_NAME = os.getenv("DB_NAME", "demo_db")
DB_USER = os.getenv("DB_USER", "demo_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "demo_password")


def get_connection():
    """
    Open a new connection to the MySQL database.

    This function is called whenever we need to talk to the DB.
    It uses the host/user/password/database we read from env vars.
    """
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    """
    Initialize the database on startup.

    What this does:
    - Waits a bit until MySQL is ready (simple retry loop).
    - Creates a table named 'items' if it does not exist.
    - Inserts one demo row into the table if it's empty.
    """
    # Try up to 10 times, waiting 2 seconds between tries
    for attempt in range(10):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Create a simple table if it does not exist yet
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id   INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                )
                """
            )

            # Check how many rows the table has
            cursor.execute("SELECT COUNT(*) FROM items")
            (count,) = cursor.fetchone()

            # If table is empty, insert one demo row
            if count == 0:
                cursor.execute("INSERT INTO items (name) VALUES ('hello-from-mysql')")
                conn.commit()

            cursor.close()
            conn.close()

            print("✅ Database initialized")
            return

        except Exception as e:
            # MySQL might not be ready yet, so wait and try again
            print(f"⏳ DB not ready yet (attempt {attempt + 1}), waiting... {e}")
            time.sleep(2)

    print("❌ Database init failed after several attempts")


# Run the database initialization when the app starts (module import time)
init_db()


@app.get("/items")
def read_items():
    """
    GET /items endpoint.

    Steps:
    1. Connect to MySQL.
    2. Run: SELECT id, name FROM items.
    3. Convert each row to a Python dict.
    4. Return the list of dicts as JSON.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Fetch all rows from the items table
        cursor.execute("SELECT id, name FROM items")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert rows from tuples to list of dicts for JSON response
        result = []
        for row in rows:
            item_id = row[0]
            item_name = row[1]
            result.append({"id": item_id, "name": item_name})

        # FastAPI automatically converts this list of dicts to JSON
        return result

    except Exception as e:
        # On error, return HTTP 500 with the error message
        raise HTTPException(status_code=500, detail=str(e))



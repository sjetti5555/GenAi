import sqlite3
import os
import bcrypt  # Ensure bcrypt is installed: pip install bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "database.db")

def connect_db():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)

def signup_user(user_data):
    """Registers a new user with a hashed password."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Hash the password securely
        hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt())

        # Insert user data into the database
        cursor.execute(
            """
            INSERT INTO users (name, email, phone, sex, country, username, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_data["name"],
                user_data["email"],
                user_data["phone"],
                user_data["sex"],
                user_data["country"],
                user_data["username"],
                hashed_password,
            ),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Signup failed: {e}")
        return False
    finally:
        conn.close()

def login_user(username, password):
    """Authenticates a user by verifying username and hashed password."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Fetch hashed password for the given username
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if not result:
            return False

        hashed_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except sqlite3.Error as e:
        print(f"Login failed: {e}")
        return False
    finally:
        conn.close()

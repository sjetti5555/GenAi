import sqlite3

def setup_database():
    """
    Sets up the SQLite database with necessary tables and constraints.
    Ensures data integrity and provides optimized queries using indexing.
    """
    try:
        # Connect to SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Create the 'users' table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            sex TEXT CHECK(sex IN ('Male', 'Female', 'Other')) NOT NULL,
            country TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create additional indexes for faster queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON users (email);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON users (username);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_country ON users (country);")

        # Commit changes and close the connection
        conn.commit()
        print("Database setup complete. 'users' table created with indexes.")
    
    except sqlite3.Error as e:
        print(f"An error occurred while setting up the database: {e}")
    
    finally:
        conn.close()

# Execute the setup
if __name__ == "__main__":
    setup_database()

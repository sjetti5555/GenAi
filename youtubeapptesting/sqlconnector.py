import mysql.connector

try:
    # Establish the connection
    conn = mysql.connector.connect(
        host="localhost",          # Replace with your host (e.g., 'localhost', '127.0.0.1')
        user="programmer",      # Replace with your MySQL username
        password="1122",  # Replace with your MySQL password
        database="mydb"   # Replace with your database name
    )
    
    # Check if the connection is successful
    if conn.is_connected():
        print("Connected to MySQL database successfully!")
    
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    # Close the connection
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("MySQL connection closed.")

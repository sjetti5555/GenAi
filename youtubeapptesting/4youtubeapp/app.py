from flask import Flask, render_template, request, redirect, url_for, session
from youtube_sentiment import extract_video_id, get_video_comments, create_csv  # Your existing functions
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

# Database Setup
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    firstname TEXT,
                    lastname TEXT,
                    sex TEXT,
                    mobile TEXT,
                    username TEXT UNIQUE,
                    password TEXT)''')
    conn.close()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    conn = sqlite3.connect('database.db')
    try:
        conn.execute("INSERT INTO users (firstname, lastname, sex, mobile, username, password) VALUES (?, ?, ?, ?, ?, ?)",
                     (data['firstname'], data['lastname'], data['sex'], data['mobile'], data['username'], data['password']))
        conn.commit()
        return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        return "Username already exists. Please try another one."
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    conn = sqlite3.connect('database.db')
    cursor = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (data['username'], data['password']))
    user = cursor.fetchone()
    conn.close()
    if user:
        session['username'] = data['username']
        return redirect(url_for('dashboard'))
    else:
        return "Invalid credentials. Try again."

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form.get('video_url')
    video_id = extract_video_id(video_url)
    comments = get_video_comments(video_id)
    csv_data = create_csv(comments)
    return render_template('results.html', data=csv_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

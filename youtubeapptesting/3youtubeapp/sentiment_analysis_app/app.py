from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import auth
import youtube_scraper
import sentiment_analysis

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

@app.route("/")
def home():
    """
    Landing page. Redirects to the dashboard if logged in.
    """
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    """
    Handles user login.
    """
    username = request.form.get("username")
    password = request.form.get("password")
    if auth.login_user(username, password):
        session["username"] = username
        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))
    flash("Invalid credentials. Please try again.", "danger")
    return redirect(url_for("home"))

@app.route("/signup", methods=["POST"])
def signup():
    """
    Handles user signup.
    """
    user_data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "sex": request.form.get("sex"),
        "country": request.form.get("country"),
        "username": request.form.get("username"),
        "password": request.form.get("password"),
    }
    if auth.signup_user(user_data):
        flash("Signup successful! You can now log in.", "success")
        return redirect(url_for("home"))
    flash("Signup failed. Username or email may already exist.", "danger")
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    """
    Displays the dashboard for logged-in users.
    """
    if "username" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("home"))
    return render_template("dashboard.html", username=session["username"])

@app.route("/logout")
def logout():
    """
    Logs out the user.
    """
    session.pop("username", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))

@app.route("/summary", methods=["POST"])
def summary():
    """
    Analyzes a YouTube video and displays a summary of sentiment analysis.
    """
    video_url = request.form.get("video_url")
    video_id = youtube_scraper.extract_video_id(video_url)
    if not video_id:
        flash("Invalid YouTube URL.", "danger")
        return redirect(url_for("dashboard"))

    video_data = youtube_scraper.get_video_data(video_id)
    if not video_data:
        flash("Failed to fetch video data. Please try again later.", "danger")
        return redirect(url_for("dashboard"))

    analysis_results = sentiment_analysis.analyze_video(video_id)
    if not analysis_results:
        flash("Sentiment analysis failed. Please try again later.", "danger")
        return redirect(url_for("dashboard"))

    return render_template(
        "summary.html",
        video_data=video_data,
        overall_sentiment=analysis_results["overall_sentiment"],
        average_score=analysis_results["average_score"],
        total_comments=analysis_results["total_comments"],
        sentiment_distribution=analysis_results["sentiment_distribution"],
    )

@app.route("/search", methods=["POST"])
def search_videos():
    """
    Searches YouTube videos by keyword and time frame.
    """
    keyword = request.form.get("keyword")
    time_frame = request.form.get("time_frame")
    print(f"Searching for keyword: {keyword} within {time_frame}")  # Debug print
    videos = youtube_scraper.search_videos_by_keyword(keyword, time_frame)
    if not videos:
        flash("No videos found for the given keyword and time frame.", "warning")
        return redirect(url_for("dashboard"))
    print(f"Found videos: {videos}")  # Debug print
    return render_template("search.html", videos=videos)

@app.route("/comments", methods=["POST"])
def analyze_comments():
    """
    Fetches and analyzes comments from a YouTube video.
    """
    video_url = request.form.get("video_url")
    video_id = youtube_scraper.extract_video_id(video_url)
    if not video_id:
        flash("Invalid YouTube URL.", "danger")
        return redirect(url_for("dashboard"))

    comments = youtube_scraper.get_video_comments(video_id)
    if not comments:
        flash("No comments found or an error occurred.", "warning")
        return redirect(url_for("dashboard"))

    analyzed_comments = [
        {
            "author": comment["author"],
            "text": comment["text"],
            "sentiment": sentiment_analysis.get_sentiment(comment["text"]),
        }
        for comment in comments
    ]
    return render_template("results.html", comments=analyzed_comments)

@app.errorhandler(404)
def page_not_found(e):
    """
    Handles 404 errors (Page Not Found).
    """
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    """
    Handles 500 errors (Server Errors).
    """
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)

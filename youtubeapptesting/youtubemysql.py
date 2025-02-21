from googleapiclient.discovery import build
from textblob import TextBlob
import mysql.connector
from datetime import datetime, timedelta

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="programmer",
        password="1122",
        database="mydb"
    )

# Save channel data to DB
def save_channel_to_db(channel_id, channel_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO channels (channel_id, channel_name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE channel_name=%s
            """,
            (channel_id, channel_name, channel_name)
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving channel: {e}")
    finally:
        cursor.close()
        conn.close()

# Save video data to DB
def save_video_to_db(video, channel_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO videos (video_id, channel_id, title, published_at, views, likes, dislikes, comments_count, rating, video_link, sentiment_score, sentiment_label)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE views=%s, likes=%s, dislikes=%s, comments_count=%s, rating=%s, sentiment_score=%s, sentiment_label=%s
            """,
            (video["Video Link"].split("v=")[-1], channel_id, video["Title"], video["Published At"],
             video["Views"], video["Likes"], video["Dislikes"], video["Comments"], video["Rating"], video["Video Link"],
             video["Sentiment"], video["Sentiment Label"],
             video["Views"], video["Likes"], video["Dislikes"], video["Comments"], video["Rating"],
             video["Sentiment"], video["Sentiment Label"])
        )
        conn.commit()
    except Exception as e:
        print(f"Error saving video: {e}")
    finally:
        cursor.close()
        conn.close()

# Save comments to DB
def save_comments_to_db(video_id, comments):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for comment in comments:
            score, label = analyze_sentiment(comment)
            cursor.execute(
                """
                INSERT INTO comments (video_id, text, sentiment_score, sentiment_label)
                VALUES (%s, %s, %s, %s)
                """,
                (video_id, comment, score, label)
            )
        conn.commit()
    except Exception as e:
        print(f"Error saving comments: {e}")
    finally:
        cursor.close()
        conn.close()

# Analyze sentiment
def analyze_sentiment(text):
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity
    label = "Positive" if score > 0.1 else "Negative" if score < -0.1 else "Neutral"
    return score, label

# Fetch channel ID
def get_channel_id(channel_name, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        response = youtube.search().list(
            part="snippet",
            q=channel_name,
            type="channel",
            maxResults=1
        ).execute()
        for item in response.get("items", []):
            if item["snippet"]["title"].lower() == channel_name.lower():
                return item["snippet"]["channelId"]
    except Exception as e:
        print(f"Error fetching channel ID: {e}")
    return None

# Fetch video stats
def get_video_stats(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        response = youtube.videos().list(part="statistics", id=video_id).execute()
        stats = response['items'][0]['statistics']
        likes = int(stats.get("likeCount", 0))
        dislikes = int(stats.get("dislikeCount", 0))
        views = int(stats.get("viewCount", 0))
        comments = int(stats.get("commentCount", 0))
        rating = likes / (likes + dislikes) if (likes + dislikes) > 0 else 0.0
        return {
            "Views": views,
            "Likes": likes,
            "Dislikes": dislikes,
            "Comments": comments,
            "Rating": round(rating, 2)
        }
    except Exception as e:
        print(f"Error fetching video stats: {e}")
        return {"Views": 0, "Likes": 0, "Dislikes": 0, "Comments": 0, "Rating": 0.0}

# Fetch videos by channel
def search_videos_by_channel(channel_id, api_key, max_results, order="date"):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    next_page_token = None
    try:
        while len(videos) < max_results:
            response = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                type="video",
                maxResults=min(50, max_results - len(videos)),
                order=order,
                pageToken=next_page_token
            ).execute()
            for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                stats = get_video_stats(video_id, api_key)
                videos.append({
                    "Video Link": f"https://www.youtube.com/watch?v={video_id}",
                    "Title": item["snippet"]["title"],
                    "Published At": item["snippet"]["publishedAt"],
                    "Views": stats["Views"],
                    "Likes": stats["Likes"],
                    "Dislikes": stats["Dislikes"],
                    "Comments": stats["Comments"],
                    "Rating": stats["Rating"]
                })
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
    except Exception as e:
        print(f"Error fetching videos: {e}")
    return videos

# Fetch comments
def fetch_comments(video_id, api_key, max_comments=100):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    next_page_token = None
    try:
        while len(comments) < max_comments:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_comments - len(comments)),
                pageToken=next_page_token
            ).execute()
            for item in response["items"]:
                comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
    except Exception as e:
        print(f"Error fetching comments: {e}")
    return comments

# Main execution
if __name__ == "__main__":
    API_KEY = "Youtube_api_key"
    channel_name = input("Enter channel name: ").strip()
    channel_id = get_channel_id(channel_name, API_KEY)

    if not channel_id:
        print(f"Channel '{channel_name}' not found. Exiting.")
        exit()

    save_channel_to_db(channel_id, channel_name)
    max_results = int(input("Enter number of videos to fetch (e.g., 10): "))
    video_results = search_videos_by_channel(channel_id, API_KEY, max_results)

    for video in video_results:
        comments = fetch_comments(video["Video Link"].split("v=")[-1], API_KEY)
        sentiment_scores = [analyze_sentiment(comment)[0] for comment in comments]
        video["Sentiment"] = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        video["Sentiment Label"] = "Positive" if video["Sentiment"] > 0.1 else "Negative" if video["Sentiment"] < -0.1 else "Neutral"
        save_video_to_db(video, channel_id)
        save_comments_to_db(video["Video Link"].split("v=")[-1], comments)

    print("Data processing completed successfully.")

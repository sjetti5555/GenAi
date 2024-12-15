from googleapiclient.discovery import build
import pandas as pd
from langdetect import detect
from transformers import pipeline
import re

# 1. Fetch Comments for a Single Video
def fetch_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100  # Fetch top 100 comments
        )
        response = request.execute()

        comments = []
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        return comments
    except Exception as e:
        if "commentsDisabled" in str(e):
            print(f"Comments are disabled for video ID: {video_id}")
        else:
            print(f"An error occurred: {e}")
        return []

# 2. Search Videos by Keyword
def search_videos(keyword, api_key, max_results=10, order="viewCount"):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.search().list(
            part="snippet",
            q=keyword,
            type="video",
            maxResults=max_results,
            order=order
        )
        response = request.execute()

        videos = []
        for item in response.get('items', []):
            video_info = {
                "Video ID": item['id']['videoId'],
                "Title": item['snippet']['title'],
                "Channel": item['snippet']['channelTitle'],
                "Published At": item['snippet']['publishedAt'],
                "Video Link": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video_info)
        return videos
    except Exception as e:
        print(f"An error occurred during video search: {e}")
        return []

# 3. Detect Language of a Comment
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# 4. Perform Sentiment Analysis
def analyze_sentiment(comments):
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"  # Multilingual sentiment model
    sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

    results = []
    for comment in comments:
        sentiment = sentiment_analyzer(comment[:512])  # Limit to 512 tokens
        results.append({
            "Comment": comment,
            "Sentiment": sentiment[0]['label'],
            "Score": sentiment[0]['score']
        })
    return results

# 5. Extract Video ID from a YouTube URL
def extract_video_id(video_link):
    match = re.search(r"v=([^&]+)", video_link)
    return match.group(1) if match else None

# Main Script with Task Selection
if __name__ == "__main__":
    API_KEY = "AIzaSyCuM07jYUqnGTjncnNop5TLz8vgZ0vSKWQ"
    
    # Select Task
    task = input("Enter task (1: Fetch comments and analyze, 2: Search for videos): ").strip()
    
    if task == "1":
        # Task 1: Fetch Comments and Analyze
        video_link = input("Enter YouTube video link: ").strip()
        video_id = extract_video_id(video_link)
        if not video_id:
            print("Invalid video link. Please provide a valid YouTube URL.")
        else:
            print(f"Fetching comments for video ID: {video_id}")
            comments = fetch_comments(video_id, API_KEY)
            if comments:
                print("Analyzing sentiment...")
                sentiment_results = analyze_sentiment(comments)

                # Convert to DataFrame and Save
                df_comments = pd.DataFrame(sentiment_results)
                df_comments.to_csv("task1_comments_sentiment.csv", index=False)
                print("Sentiment analysis results saved to 'task1_comments_sentiment.csv'.")
            else:
                print("No comments available for analysis.")
    
    elif task == "2":
        # Task 2: Search for Videos
        keyword = input("Enter a keyword to search videos: ").strip()
        order = input("Enter order preference ('date' for recent, 'viewCount' for most viewed): ").strip()
        if order not in ["date", "viewCount"]:
            order = "viewCount"  # Default to most viewed

        print(f"Searching videos for keyword: {keyword} (Order: {order})")
        video_results = search_videos(keyword, API_KEY, max_results=10, order=order)

        if video_results:
            df_videos = pd.DataFrame(video_results)
            df_videos.to_csv("task2_video_results.csv", index=False)
            print("Video search results saved to 'task2_video_results.csv'.")
            print(df_videos)
        else:
            print("No videos found for the given keyword.")
    else:
        print("Invalid task selection. Please enter 1 or 2.")

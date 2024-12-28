import re
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

API_KEY = ""  # Replace with your actual API key
youtube = build("youtube", "v3", developerKey=API_KEY)

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    match = re.search(r"(?<=v=)[^&#]+", url)
    return match.group(0) if match else None

def get_video_data(video_id):
    """Fetch video metadata using the YouTube API."""
    try:
        request = youtube.videos().list(part="snippet,statistics", id=video_id)
        response = request.execute()
        video_info = response["items"][0]
        return {
            "title": video_info["snippet"]["title"],
            "description": video_info["snippet"]["description"],
            "views": int(video_info["statistics"].get("viewCount", 0)),
            "likes": int(video_info["statistics"].get("likeCount", 0)),
            "comments": int(video_info["statistics"].get("commentCount", 0)),
        }
    except Exception as e:
        print(f"Error fetching video data: {e}")
        return None

def get_video_comments(video_id):
    """Fetch top-level comments for a video."""
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet", videoId=video_id, maxResults=100, textFormat="plainText"
        )
        while request:
            response = request.execute()
            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": snippet["authorDisplayName"],
                    "text": snippet["textDisplay"],
                })
            request = youtube.commentThreads().list_next(request, response)
    except Exception as e:
        print(f"Error fetching comments: {e}")
    return comments

def search_videos_by_keyword(keyword, published_after):
    """Search videos by keyword and time frame."""
    try:
        request = youtube.search().list(
            part="snippet",
            q=keyword,
            maxResults=10,
            publishedAfter=published_after,
            type="video",
        )
        
        response = request.execute()
        videos = [
            {
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            }
            for item in response["items"]
        ]
        return videos
    except Exception as e:
        print(f"Error searching videos: {e}")
        return None

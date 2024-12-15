import re
from googleapiclient.discovery import build
from datetime import datetime, timedelta

api_key = 'AIzaSyCuM07jYUqnGTjncnNop5TLz8vgZ0vSKWQ'
youtube = build('youtube', 'v3', developerKey=api_key)

def extract_video_id(url):
    match = re.search(r"(?<=v=)[^&#]+", url)
    return match.group(0) if match else None

def get_video_comments(video_id, max_results=100):
    comments = []
    request = youtube.commentThreads().list(
        part='snippet', 
        videoId=video_id, 
        textFormat='plainText', 
        maxResults=max_results
    )
    response = request.execute()
    for item in response.get('items', []):
        snippet = item['snippet']['topLevelComment']['snippet']
        comments.append({
            'author': snippet['authorDisplayName'],
            'text': snippet['textDisplay'],
            'published_at': snippet['publishedAt']
        })
    return comments

def get_videos_by_keyword(keyword, time_filter):
    published_after = (datetime.utcnow() - timedelta(seconds=time_filter)).isoformat("T") + "Z"
    request = youtube.search().list(
        part='snippet',
        q=keyword,
        type='video',
        publishedAfter=published_after,
        maxResults=50
    )
    response = request.execute()
    videos = [
        {'title': item['snippet']['title'], 'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"}
        for item in response.get('items', [])
    ]
    return videos

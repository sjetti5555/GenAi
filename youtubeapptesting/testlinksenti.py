from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta
import time
from textblob import TextBlob  # Install this library if not already available

def get_channel_id(channel_name, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.search().list(
            part="snippet",
            q=channel_name,
            type="channel",
            maxResults=10
        )
        response = request.execute()
        for item in response.get("items", []):
            if item["snippet"]["title"] == channel_name:
                print(f"Exact match found: {item['snippet']['channelId']}")
                return item["snippet"]["channelId"]
        print(f"No exact match found for channel name: {channel_name}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def calculate_date_filter_dynamic(time_value, time_unit):
    now = datetime.utcnow()
    if time_unit == "minute":
        delta = timedelta(minutes=time_value)
    elif time_unit == "hour":
        delta = timedelta(hours=time_value)
    elif time_unit == "day":
        delta = timedelta(days=time_value)
    else:
        print("Invalid time unit! Defaulting to 1 day.")
        delta = timedelta(days=1)
    max_delta = timedelta(days=30)
    if delta > max_delta:
        delta = max_delta
        print("Time range exceeds 1 month. Limiting to 1 month.")
    published_after = now - delta
    return {
        "publishedAfter": published_after.isoformat("T") + "Z",
        "publishedBefore": now.isoformat("T") + "Z"
    }

def get_video_stats(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        response = request.execute()
        stats = response['items'][0]['statistics']
        likes = int(stats.get("likeCount", 0))
        dislikes = int(stats.get("dislikeCount", 0))  # Assumes dislikes are available
        views = int(stats.get("viewCount", 0))
        comments = int(stats.get("commentCount", 0))
        rating = likes / (likes + dislikes) if (likes + dislikes) > 0 else 0  # Calculate rating
        return {
            "Views": views,
            "Likes": likes,
            "Dislikes": dislikes,
            "Comments": comments,
            "Rating": round(rating, 2)
        }
    except Exception as e:
        print(f"Failed to fetch stats for video {video_id}: {e}")
        return {"Views": 0, "Likes": 0, "Dislikes": 0, "Comments": 0, "Rating": 0}

def search_videos_by_channel(channel_id, api_key, max_results, order="date", date_filter=None):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    next_page_token = None

    while len(videos) < max_results:
        try:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                type="video",
                maxResults=min(50, max_results - len(videos)),
                order=order,
                pageToken=next_page_token,
                publishedAfter=date_filter.get('publishedAfter') if date_filter else None,
                publishedBefore=date_filter.get('publishedBefore') if date_filter else None
            )
            response = request.execute()
            for item in response.get('items', []):
                video_id = item['id']['videoId']
                stats = get_video_stats(video_id, api_key)
                video_info = {
                    "Title": item['snippet']['title'],
                    "Channel": item['snippet']['channelTitle'],
                    "Published At": item['snippet']['publishedAt'],
                    "Views": stats["Views"],
                    "Likes": stats["Likes"],
                    "Dislikes": stats["Dislikes"],
                    "Comments": stats["Comments"],
                    "Rating": stats["Rating"],
                    "Video Link": f"https://www.youtube.com/watch?v={video_id}"
                }
                videos.append(video_info)
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        except Exception as e:
            print(f"Error while fetching videos: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
            continue

    return videos

def fetch_comments(video_id, api_key, max_comments=100):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_comments - len(comments)),
                pageToken=next_page_token
            )
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")
            break

    return comments

def analyze_sentiment(text):
    analysis = TextBlob(text)
    score = analysis.sentiment.polarity  # Sentiment score between -1 (negative) to 1 (positive)
    if score > 0.1:
        label = "Positive"
    elif score < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
    return score, label

def add_sentiment_to_videos(video_data, api_key):
    for video in video_data:
        video_id = video["Video Link"].split("v=")[-1]
        comments = fetch_comments(video_id, api_key, max_comments=100)
        if comments:
            sentiment_scores = [analyze_sentiment(comment)[0] for comment in comments]
            avg_score = sum(sentiment_scores) / len(sentiment_scores)
            _, sentiment_label = analyze_sentiment(" ".join(comments))
        else:
            avg_score = 0
            sentiment_label = "Neutral"

        video["Sentiment"] = avg_score
        video["Sentiment Label"] = sentiment_label

    return video_data

if __name__ == "__main__":
    API_KEY = "Youtube_api_key"
    channel_name = input("Enter the channel name (case-sensitive and space-sensitive): ").strip()
    channel_id = get_channel_id(channel_name, API_KEY)
    if not channel_id:
        print(f"Channel name '{channel_name}' not found. Please try again.")
        exit()
    print(f"Channel ID for '{channel_name}' retrieved successfully: {channel_id}")
    order = input("Enter order preference ('date', 'viewCount', 'relevance', 'rating'): ").strip().lower()
    if order not in ["date", "viewCount", "relevance", "rating"]:
        order = "date"
    max_results = int(input("Enter the number of results you want (e.g., 10, 50, 100, 500): "))
    if max_results > 500:
        max_results = 500
        print("Maximum limit is 500 results. Limiting to 500.")
    time_value = int(input("Enter the time range value (e.g., 1, 5, 10): "))
    time_unit = input("Enter the time unit ('minute', 'hour', 'day'): ").strip()
    date_filter = calculate_date_filter_dynamic(time_value, time_unit)
    print(f"Searching {max_results} videos from channel '{channel_name}' (Order: {order})")
    video_results = search_videos_by_channel(channel_id, API_KEY, max_results, "date", date_filter)
    print("Performing sentiment analysis on video comments...")
    enhanced_video_results = add_sentiment_to_videos(video_results, API_KEY)
    df_videos_with_sentiment = pd.DataFrame(enhanced_video_results)
    print("Sentiment analysis completed.")
    print(df_videos_with_sentiment)
    filename = f"yt_channel_sentiment_{channel_name.replace(' ', '_')}_{max_results}results.csv"
    df_videos_with_sentiment.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Results with sentiment analysis saved to '{filename}'.")

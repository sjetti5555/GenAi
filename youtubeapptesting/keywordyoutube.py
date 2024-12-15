from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta

def get_video_statistics(video_ids, api_key):
    """
    Fetch statistics for a list of video IDs.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    stats_request = youtube.videos().list(
        part="statistics",
        id=",".join(video_ids)
    )
    stats_response = stats_request.execute()

    video_stats = {}
    for item in stats_response.get('items', []):
        video_id = item['id']
        video_stats[video_id] = {
            "Likes": int(item['statistics'].get('likeCount', 0)),
            "Comments": int(item['statistics'].get('commentCount', 0)),
            "Views": int(item['statistics'].get('viewCount', 0))
        }
    return video_stats

def calculate_date_filter_dynamic(time_value, time_unit):
    """
    Calculate 'publishedAfter' and 'publishedBefore' dynamically with a max limit of 1 month.
    """
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

    # Constrain to a maximum of 1 month
    max_delta = timedelta(days=30)
    if delta > max_delta:
        delta = max_delta
        print("Time range exceeds 1 month. Limiting to 1 month.")

    published_after = now - delta
    return {
        "publishedAfter": published_after.isoformat("T") + "Z",
        "publishedBefore": now.isoformat("T") + "Z"
    }

def search_videos(keyword, api_key, max_results, order="viewCount", date_filter=None):
    """
    Search for videos on YouTube by keyword with an optional date filter.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []
    next_page_token = None

    while len(videos) < max_results:
        request = youtube.search().list(
            part="snippet",
            q=keyword,
            type="video",
            maxResults=min(50, max_results - len(videos)),  # Fetch up to 50 per request
            order=order,
            pageToken=next_page_token,
            publishedAfter=date_filter.get('publishedAfter') if date_filter else None,
            publishedBefore=date_filter.get('publishedBefore') if date_filter else None
        )
        response = request.execute()

        video_ids = [item['id']['videoId'] for item in response.get('items', [])]
        video_stats = get_video_statistics(video_ids, api_key)

        for item in response.get('items', []):
            video_id = item['id']['videoId']
            stats = video_stats.get(video_id, {"Likes": 0, "Comments": 0, "Views": 0})

            video_info = {
                "Title": item['snippet']['title'],
                "Channel": item['snippet']['channelTitle'],
                "Published At": item['snippet']['publishedAt'],
                "Likes": stats["Likes"],
                "Comments": stats["Comments"],
                "Views": stats["Views"],
                "Video Link": f"https://www.youtube.com/watch?v={video_id}"
            }
            videos.append(video_info)

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos


# Main Script
if __name__ == "__main__":
    # API Key
    API_KEY = "AIzaSyCMx6x5zWLPcZ7MBo4d94Sq-pPZ1K10zIo"

    # Input Keyword and Search Preference
    keyword = input("Enter a keyword to search videos: ")
    order = input("Enter order preference ('date', 'viewCount', 'likes'): ").strip()
    if order not in ["date", "viewCount", "likes"]:
        order = "viewCount"

    # Input Number of Results
    max_results = int(input("Enter the number of results you want (e.g., 12, 50, 100, 500): "))
    if max_results > 500:
        max_results = 500
        print("Maximum limit is 500 results. Limiting to 500.")

    # Time Range Input
    time_value = int(input("Enter the time range value (e.g., 1, 5, 10): "))
    time_unit = input("Enter the time unit ('minute', 'hour', 'day'): ").strip()
    date_filter = calculate_date_filter_dynamic(time_value, time_unit)

    print(f"Searching {max_results} videos for keyword: {keyword} (Order: {order})")
    video_results = search_videos(keyword, API_KEY, max_results=max_results, order="viewCount" if order == "likes" else order, date_filter=date_filter)

    # Sort by likes if required
    if order == "likes":
        video_results = sorted(video_results, key=lambda x: x["Likes"], reverse=True)

    # Convert to DataFrame and Display
    df_videos = pd.DataFrame(video_results)
    print(f"Top {max_results} Videos Found ({order}):")
    print(df_videos)

    # Save to CSV with dynamic filename
    filename = f"yt_{order}_{keyword.replace(' ', '_')}_{max_results}results.csv"
    df_videos.to_csv(filename, index=False)
    print(f"Results saved to '{filename}'.")

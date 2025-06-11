import pandas as pd
from googleapiclient.discovery import build
from langdetect import detect
from transformers import pipeline

# 1. Function to Fetch Comments using YouTube Data API
# Fetch All Comments Using Pagination
def fetch_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    next_page_token = None

    while True:
        try:
            # Request comments with pagination
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token  # Get the next page of comments
            )
            response = request.execute()

            # Extract comments
            for item in response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # Check if there's another page of comments
            next_page_token = response.get('nextPageToken')
            if not next_page_token:  # No more pages
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return comments


# 2. Detect Language of the Comment
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# 3. Perform Sentiment Analysis
def analyze_sentiment(comments):
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"  # Pretrained multilingual sentiment model
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

# 4. Main Script
if __name__ == "__main__":
    # API Key and Video ID
    API_KEY = "Youtube API Key"
    VIDEO_ID = "EGF8PUQwXGc"

    print("Fetching comments...")
    comments = fetch_comments(VIDEO_ID, API_KEY)
    print(f"Total comments fetched: {len(comments)}")

    print("Detecting languages...")
    comments_data = [{"Comment": comment, "Language": detect_language(comment)} for comment in comments]

    print("Analyzing sentiment...")
    sentiment_results = analyze_sentiment([item['Comment'] for item in comments_data])

    # Combine language and sentiment data
    for i, item in enumerate(sentiment_results):
        item['Language'] = comments_data[i]['Language']

    # Convert to DataFrame and save results
    df = pd.DataFrame(sentiment_results)
    print("Analysis Complete!")
    print(df.head())

    # Save to CSV
    df.to_csv("data/youtube_comments_sentiment.csv", index=False)
    print("Results saved to 'data/youtube_comments_sentiment.csv'.")

import pandas as pd
from googleapiclient.discovery import build
from transformers import pipeline
from transformers import AutoTokenizer
from tqdm import tqdm
import re
import os

# 1. Function to Fetch Comments and Authors using YouTube Data API
def fetch_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    next_page_token = None

    while True:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response.get('items', []):
                snippet = item['snippet']['topLevelComment']['snippet']
                comment = snippet['textDisplay']
                author = snippet['authorDisplayName']
                if comment.strip():  # Skip empty comments
                    comments.append({"Comment": comment, "Author": author})

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        except Exception as e:
            if "quotaExceeded" in str(e):
                print("YouTube API quota exceeded. Try again later.")
            else:
                print(f"An error occurred: {e}")
            break

    return comments

# 2. Clean Comments
def clean_comment(text):
    # Remove special characters, links, and extra spaces
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r"[^a-zA-Z0-9\u0C00-\u0C7F\u0900-\u097F\u0B80-\u0BFF\u0C80-\u0CFF\s]", '', text)  # Keep English, numbers, and Telugu, Kannada, Tamil, Hindi Characters

    return text.strip()

def analyze_sentiment_batched(comments, batch_size=32):
    model_name = "cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    sentiment_analyzer = pipeline("sentiment-analysis", model=model_name, tokenizer=tokenizer)

    # Truncate comments based on token length
    truncated_comments = []
    for comment in comments:
        tokens = tokenizer.encode(comment, truncation=True, max_length=512)
        truncated_comments.append(tokenizer.decode(tokens, skip_special_tokens=True))

    results = []
    for i in tqdm(range(0, len(truncated_comments), batch_size), desc="Analyzing Sentiment"):
        batch = truncated_comments[i:i + batch_size]
        sentiments = sentiment_analyzer(batch)
        results.extend(sentiments)
    return results


def determine_sentiment_label(sentiment):
    if sentiment == "LABEL_0":
        return "Negative"
    elif sentiment == "LABEL_1":
        return "Neutral"
    else:
        return "Positive"


# 5. Calculate Overall Sentiment Summary
def calculate_overall_summary(df):
    total_comments = len(df)
    positive = len(df[df["Sentiment Label"] == "Positive"])
    neutral = len(df[df["Sentiment Label"] == "Neutral"])
    negative = len(df[df["Sentiment Label"] == "Negative"])

    overall_score = df["Score"].mean() if total_comments > 0 else 0

    return {
        "Total Comments": total_comments,
        "Analyzed Comments": total_comments,
        "Overall Score": round(overall_score, 2),
        "Positive Comments": positive,
        "Neutral Comments": neutral,
        "Negative Comments": negative,
    }

# 6. Main Script
if __name__ == "__main__":
    # API Key and Input from User
    API_KEY = "Youtube API Key"
    VIDEO_ID = input("Enter YouTube video ID: ").strip()

    print("Fetching comments...")
    comments_data = fetch_comments(VIDEO_ID, API_KEY)
    print(f"Total comments fetched: {len(comments_data)}")

    print("Cleaning comments...")
    for item in comments_data:
        item["Cleaned Comment"] = clean_comment(item["Comment"])

    print("Analyzing sentiment...")
    sentiment_results = analyze_sentiment_batched([item['Cleaned Comment'] for item in comments_data])

    # Combine sentiment data with existing comment data
    for i, sentiment in enumerate(sentiment_results):
        comments_data[i]['Sentiment'] = sentiment['label']
        comments_data[i]['Score'] = sentiment['score']
        comments_data[i]['Sentiment Label'] = determine_sentiment_label(sentiment['label'])

    # Convert to DataFrame
    df = pd.DataFrame(comments_data)

    # Calculate Overall Sentiment Summary
    overall_summary = calculate_overall_summary(df)

     # Generate file name based on video ID
    output_file = f"youtube_comments_analysis_{VIDEO_ID}.csv"

    # Check if file already exists
    file_exists = os.path.isfile(output_file)

    # Save to CSV (Append if exists, else create new file)
    df.to_csv(output_file, mode='a', header=not file_exists, index=False, columns=["Author", "Comment", "Cleaned Comment", "Sentiment", "Score", "Sentiment Label"])


    # Confirm file save
    if file_exists:
        print(f"Results appended to '{output_file}'.")
    else:
        print(f"Results saved to '{output_file}'.")

    # Print Overall Summary
    print("\nOverall Sentiment Summary:")
    for key, value in overall_summary.items():
        print(f"{key}: {value}")

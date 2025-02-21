import os
import re
import pandas as pd
from googleapiclient.discovery import build
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline

# NLTK Downloads
nltk.download('punkt')
nltk.download('stopwords')

# Initialize YouTube API
api_key = 'Youtube_api_key'  # Replace with your YouTube Data API key
youtube = build('youtube', 'v3', developerKey=api_key)

# Initialize sentiment analysis model
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

def extract_video_id(url):
    match = re.search(r"(?<=v=)[^&#]+", url)
    match = match or re.search(r"(?<=be/)[^&#]+", url)
    video_id = match.group(0) if match else None
    return video_id

def get_video_comments(video_id):
    comments = []
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100
    ).execute()

    while response:
        for item in response['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            timestamp = item['snippet']['topLevelComment']['snippet']['publishedAt']
            comments.append((author_name, comment_text, timestamp))

        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                pageToken=response['nextPageToken'],
                textFormat='plainText',
                maxResults=100
            ).execute()
        else:
            break

    return comments

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    tokenized = word_tokenize(text)
    tokenized = [word for word in tokenized if word not in stopwords.words('english')]
    return ' '.join(tokenized)

def get_sentiment(text):
    try:
        result = sentiment_analyzer(text)[0]  # Get the first (and only) result
        return result['label'], result['score']  # Return both sentiment label and score
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "Neutral", 0  # Default sentiment in case of any error

def save_comments_to_csv(comments, filename):
    df = pd.DataFrame(comments, columns=['AuthorName', 'Comment', 'Timestamp'])
    df['Cleaned_Comment'] = df['Comment'].apply(clean_text)
    df[['Sentiment_Class', 'Sentiment_Score']] = df['Cleaned_Comment'].apply(lambda x: pd.Series(get_sentiment(x)))
    df.sort_values(by='Timestamp', inplace=True)
    df.to_csv(filename, index=False)

def main():
    video_url = input("Enter the YouTube video URL: ")
    video_id = extract_video_id(video_url)
    if video_id:
        comments = get_video_comments(video_id)
        save_comments_to_csv(comments, f'{video_id}_sentiment_analysis.csv')
        print("Sentiment analysis complete. Results saved to CSV.")
    else:
        print("Invalid YouTube URL")

if __name__ == '__main__':
    main()

import os
import re
import pandas as pd
from textblob import TextBlob
from googleapiclient.discovery import build
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# NLTK Downloads
nltk.download('punkt')
nltk.download('stopwords')

# Initialize YouTube API
api_key = 'AIzaSyCuM07jYUqnGTjncnNop5TLz8vgZ0vSKWQ'  # Replace with your YouTube Data API key
youtube = build('youtube', 'v3', developerKey=api_key)

def extract_video_id(url):
    # Extract the video ID from a YouTube URL
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
        order='time',  # Attempt to order by time, though the default should already be newest first
        maxResults=100
    ).execute()

    while response:
        for item in response['items']:
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            timestamp = item['snippet']['topLevelComment']['snippet']['publishedAt']  # Getting the timestamp
            comments.append((author_name, comment_text, timestamp))

        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                pageToken=response['nextPageToken'],
                textFormat='plainText',
                order='time',  # Maintain the order through pagination
                maxResults=100
            ).execute()
        else:
            break

    return comments

def clean_text(text):
    text = text.lower()  # convert to lowercase
    text = re.sub(r'\d+', '', text)  # remove numbers
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # remove URLs
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)  # remove special characters
    tokenized = word_tokenize(text)
    tokenized = [word for word in tokenized if word not in stopwords.words('english')]
    return ' '.join(tokenized)

def classify_sentiment(polarity):
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns a polarity score between -1 and 1

def save_comments_to_csv(comments, filename):
    df = pd.DataFrame(comments, columns=['AuthorName', 'Comment', 'Timestamp'])
    df['Cleaned_Comment'] = df['Comment'].apply(clean_text)
    df['Sentiment_Score'] = df['Cleaned_Comment'].apply(get_sentiment)
    df['Sentiment_Class'] = df['Sentiment_Score'].apply(classify_sentiment)
    df.sort_values(by='Timestamp', inplace=True)
    # Get the current working directory
    current_directory = os.getcwd()
    filepath = os.path.join(current_directory, filename)
    df.to_csv(filepath, index=False)

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

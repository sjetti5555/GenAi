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
        maxResults=100
    ).execute()

    while response:
        for item in response['items']:
            author_channel_id = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append((comment_text, author_channel_id))

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
    text = text.lower()  # convert to lowercase
    text = re.sub(r'\d+', '', text)  # remove numbers
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # remove URLs
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)  # remove special characters
    tokenized = word_tokenize(text)
    tokenized = [word for word in tokenized if word not in stopwords.words('english')]
    return ' '.join(tokenized)

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns a polarity score between -1 and 1

def save_comments_to_csv(comments, filename):
    df = pd.DataFrame(comments, columns=[ 'AuthorChannelID', 'Comment',])
    df['Cleaned_Comment'] = df['Comment'].apply(clean_text)
    df['Sentiment'] = df['Cleaned_Comment'].apply(get_sentiment)
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
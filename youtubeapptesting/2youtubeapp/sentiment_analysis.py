import re
import pandas as pd
from googleapiclient.discovery import build
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline
from langdetect import detect, LangDetectException

# Initialize API and sentiment analysis
api_key = 'Youtube_APi_key'
youtube = build('youtube', 'v3', developerKey=api_key)
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

def extract_video_id(url):
    match = re.search(r"(?<=v=)[^&#]+", url)
    return match.group(0) if match else None

def get_video_comments(video_id):
    comments = []
    request = youtube.commentThreads().list(part='snippet', videoId=video_id, textFormat='plainText', maxResults=100)
    response = request.execute()
    for item in response.get('items', []):
        comment = item['snippet']['topLevelComment']['snippet']
        text = clean_text(comment['textDisplay'])
        if len(text.split()) > 0:  # Check if text has enough words
            try:
                language = detect(text)
                if language == 'en':
                    sentiment_result = get_sentiment(text)
                    comments.append((comment['authorDisplayName'], comment['textDisplay'], comment['publishedAt'], sentiment_result[0], sentiment_result[1]))
            except LangDetectException:
                print("Language detection failed for text:", text)
    return comments

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    tokens = word_tokenize(text)
    return ' '.join(word for word in tokens if word not in stopwords.words('english'))

def get_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return result['label'], round(result['score'], 2)

def create_csv(comments):
    df = pd.DataFrame(comments, columns=['AuthorName', 'Comment', 'Timestamp', 'Sentiment_Class', 'Sentiment_Score'])
    return df.to_csv(index=False)

import datetime
import pandas as pd
import schedule
import time
import os
import numpy as np
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# Download required NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# API setup
API_KEY = 'AIzaSyADnCA_k6P_mfndvl55k9ypNXk3WFKQSrY'
VIDEO_ID = 'cG18_T-EsA4'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_comments():
    """Fetches comments from the YouTube video."""
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=VIDEO_ID,
            maxResults=100,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        
        return comments
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def preprocess_text(text):
    """Preprocess text for analysis."""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenization
    tokens = text.split()
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens

def analyze_text(comments):
    """Perform comprehensive text analysis on comments."""
    all_tokens = []
    analysis_results = {
        'word_freq': Counter(),
        'avg_word_length': [],
        'sentiment_scores': [],
        'subjectivity_scores': [],
        'processed_comments': []
    }
    
    for comment in comments:
        # Tokenization and preprocessing
        tokens = preprocess_text(comment)
        all_tokens.extend(tokens)
        analysis_results['word_freq'].update(tokens)
        
        # Word length analysis
        analysis_results['avg_word_length'].append(
            np.mean([len(word) for word in tokens]) if tokens else 0
        )
        
        # Sentiment Analysis using TextBlob
        blob = TextBlob(comment)
        analysis_results['sentiment_scores'].append(blob.sentiment.polarity)
        analysis_results['subjectivity_scores'].append(blob.sentiment.subjectivity)
        
        # Store processed comment
        analysis_results['processed_comments'].append(' '.join(tokens))
    
    return analysis_results, all_tokens

def generate_visualizations(analysis_results, all_tokens):
    """Generate visualizations for text analysis results."""
    # Word Cloud
    if all_tokens:
        plt.figure(figsize=(12, 8))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(all_tokens))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Comments')
        plt.show()
    
    # Top Words Frequency
    if analysis_results['word_freq']:
        plt.figure(figsize=(12, 6))
        words, counts = zip(*analysis_results['word_freq'].most_common(10))
        plt.bar(words, counts)
        plt.xticks(rotation=45)
        plt.title('Top 10 Most Frequent Words')
        plt.tight_layout()
        plt.show()
    
    # Sentiment Distribution
    if analysis_results['sentiment_scores']:
        plt.figure(figsize=(10, 6))
        plt.hist(analysis_results['sentiment_scores'], bins=20)
        plt.title('Distribution of Sentiment Scores')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Frequency')
        plt.show()
    
    # Subjectivity vs Sentiment Scatter Plot
    if analysis_results['sentiment_scores'] and analysis_results['subjectivity_scores']:
        plt.figure(figsize=(10, 6))
        plt.scatter(analysis_results['sentiment_scores'], analysis_results['subjectivity_scores'])
        plt.title('Sentiment vs Subjectivity')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Subjectivity Score')
        plt.show()

def print_analysis_summary(analysis_results):
    """Print summary of text analysis."""
    print("\nText Analysis Summary:")
    print("-" * 50)
    
    if analysis_results['word_freq']:
        print("\nTop 10 Most Common Words:")
        for word, count in analysis_results['word_freq'].most_common(10):
            print(f"{word}: {count}")
    
    if analysis_results['sentiment_scores']:
        print("\nSentiment Analysis:")
        avg_sentiment = np.mean(analysis_results['sentiment_scores'])
        avg_subjectivity = np.mean(analysis_results['subjectivity_scores'])
        print(f"Average Sentiment Score: {avg_sentiment:.2f}")
        print(f"Average Subjectivity Score: {avg_subjectivity:.2f}")
    
    if analysis_results['avg_word_length']:
        print("\nAverage Word Length:")
        avg_length = np.mean(analysis_results['avg_word_length'])
        print(f"Average words length: {avg_length:.2f}")

def job():
    """Main job function."""
    print("Fetching comments...")
    comments = fetch_comments()
    
    if comments:
        print(f"Found {len(comments)} comments")
        print("Performing text analysis...")
        
        # Perform text analysis
        analysis_results, all_tokens = analyze_text(comments)
        
        # Generate visualizations
        generate_visualizations(analysis_results, all_tokens)
        
        # Print analysis summary
        print_analysis_summary(analysis_results)
        
        print("Analysis completed.")
    else:
        print("No comments found or error occurred.")

# Run initial analysis
print("Starting initial analysis...")
job()

# Schedule regular updates
schedule.every(15).minutes.do(job)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

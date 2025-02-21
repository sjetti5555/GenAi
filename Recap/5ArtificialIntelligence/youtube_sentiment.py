import pandas as pd
import numpy as np
from googleapiclient.discovery import build
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import datetime
import schedule
import time

# Download required NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

class YouTubeSentimentAnalyzer:
    def __init__(self, api_key, video_id):
        self.api_key = 'Your API Key'
        self.video_id = '1SMlSLeIM7E'
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.comments = []
        self.all_comments = set()  # Store all unique comments
        self.sentiment_data = None
        self.last_fetch_time = None
        
    def fetch_comments(self, is_initial=False):
        """Fetch comments from YouTube video"""
        try:
            current_time = datetime.datetime.now()
            
            request_params = {
                "part": "snippet",
                "videoId": self.video_id,
                "maxResults": 100 if is_initial else 50,  # Get more comments initially
                "textFormat": "plainText",
                "order": "time"
            }
            
            if not is_initial and self.last_fetch_time:
                time_diff = current_time - self.last_fetch_time
                if time_diff.total_seconds() < 900:  # 15 minutes
                    print(f"Waiting for more time to pass. Next fetch in {15 - time_diff.total_seconds()/60:.1f} minutes")
                    return False
            
            request = self.youtube.commentThreads().list(**request_params)
            response = request.execute()
            
            new_comments = []
            for item in response['items']:
                comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
                if comment_text not in self.all_comments:  # Check for uniqueness
                    new_comments.append(comment_text)
                    self.all_comments.add(comment_text)
            
            self.comments = list(self.all_comments)  # Update with all unique comments
            self.last_fetch_time = current_time
            
            print(f"Fetched {len(new_comments)} new comments")
            print(f"Total unique comments: {len(self.all_comments)}")
            return True
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def preprocess_text(self, text):
        """Clean and preprocess text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = text.split()
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if t not in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
        return ' '.join(tokens)

    def analyze_sentiment(self):
        """Perform sentiment analysis on comments"""
        if not self.comments:
            print("No comments to analyze")
            return False

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        analysis_results = []
        for comment in self.comments:
            processed_comment = self.preprocess_text(comment)
            blob = TextBlob(comment)
            
            sentiment_score = blob.sentiment.polarity
            subjectivity_score = blob.sentiment.subjectivity
            
            if sentiment_score > 0:
                sentiment_category = 'Positive'
            elif sentiment_score < 0:
                sentiment_category = 'Negative'
            else:
                sentiment_category = 'Neutral'
            
            analysis_results.append({
                'timestamp': current_time,
                'original_comment': comment,
                'processed_comment': processed_comment,
                'sentiment_score': sentiment_score,
                'subjectivity_score': subjectivity_score,
                'sentiment_category': sentiment_category,
                'word_count': len(processed_comment.split())
            })

        self.sentiment_data = pd.DataFrame(analysis_results)
        
        # Save to CSV (overwrite mode for cumulative analysis)
        csv_filename = f'youtube_comments_{self.video_id}_cumulative.csv'
        self.sentiment_data.to_csv(csv_filename, index=False)
        
        print(f"Cumulative analysis saved to {csv_filename}")
        return True

    def generate_visualizations(self):
        """Generate visualizations for sentiment analysis"""
        if self.sentiment_data is None:
            print("No data to visualize")
            return

        # 1. Sentiment Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(self.sentiment_data['sentiment_score'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribution of Sentiment Scores')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Count')
        plt.show()

        # 2. Sentiment Categories Pie Chart
        plt.figure(figsize=(8, 8))
        sentiment_counts = self.sentiment_data['sentiment_category'].value_counts()
        plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', 
                colors=['lightgreen', 'lightcoral', 'lightskyblue'])
        plt.title('Distribution of Sentiment Categories')
        plt.show()

        # 3. Word Cloud
        all_words = ' '.join(self.sentiment_data['processed_comment'])
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of Comments')
        plt.show()

        # 4. Sentiment vs Subjectivity Scatter Plot
        plt.figure(figsize=(10, 6))
        colors = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'blue'}
        for category in colors:
            mask = self.sentiment_data['sentiment_category'] == category
            plt.scatter(
                self.sentiment_data[mask]['sentiment_score'],
                self.sentiment_data[mask]['subjectivity_score'],
                c=colors[category],
                label=category,
                alpha=0.6
            )
        plt.title('Sentiment vs Subjectivity')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Subjectivity Score')
        plt.legend()
        plt.show()

    def print_summary(self):
        """Print summary statistics of the analysis"""
        if self.sentiment_data is None:
            print("No data to summarize")
            return

        print("\n=== YouTube Comment Sentiment Analysis Summary ===")
        print(f"Video ID: {self.video_id}")
        print(f"Total Comments Analyzed: {len(self.sentiment_data)}")
        
        print("\nSentiment Distribution:")
        sentiment_dist = self.sentiment_data['sentiment_category'].value_counts()
        for category, count in sentiment_dist.items():
            percentage = (count/len(self.sentiment_data))*100
            print(f"{category}: {count} comments ({percentage:.1f}%)")
        
        print("\nSentiment Score Statistics:")
        print(f"Average Sentiment Score: {self.sentiment_data['sentiment_score'].mean():.3f}")
        print(f"Median Sentiment Score: {self.sentiment_data['sentiment_score'].median():.3f}")
        
        print("\nSubjectivity Statistics:")
        print(f"Average Subjectivity Score: {self.sentiment_data['subjectivity_score'].mean():.3f}")
        
        print("\nWord Count Statistics:")
        print(f"Average Words per Comment: {self.sentiment_data['word_count'].mean():.1f}")

def analyze_job(api_key, video_id, is_initial=False):
    """Job to be run every 15 minutes"""
    analyzer = YouTubeSentimentAnalyzer(api_key, video_id)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n=== Analysis Cycle at {current_time} ===")
    if analyzer.fetch_comments(is_initial):
        analyzer.analyze_sentiment()
        analyzer.print_summary()
        analyzer.generate_visualizations()
    print("\nWaiting for next analysis cycle...")

def main():
    # YouTube API credentials
    API_KEY = 'Youtube_api_key'
    VIDEO_ID = 'Youtube_video_id'
    
    print("Starting YouTube Comment Sentiment Analysis")
    print(f"Video URL: https://www.youtube.com/watch?v={VIDEO_ID}")
    print("Initial analysis of first 100 comments, then cumulative updates every 15 minutes")
    
    # Run initial analysis with first 100 comments
    print("\nRunning initial analysis...")
    analyze_job(API_KEY, VIDEO_ID, is_initial=True)

    # Schedule the job to run every 15 minutes
    schedule.every(3).minutes.do(analyze_job, API_KEY, VIDEO_ID, False)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nAnalysis stopped by user")

if __name__ == "__main__":
    main() 

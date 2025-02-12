import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import re
from datetime import datetime

# Download NLTK data
nltk.download('stopwords')
nltk.download('punkt')

def setup_driver():
    """Setup Chrome WebDriver with options"""
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Create Service object
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_tweets(driver, tweet_url, num_tweets=100):
    """Fetch replies from the tweet"""
    try:
        driver.get( 'https://x.com/KonstantinKisin' )
        time.sleep(1)  # Wait for page to load
        
        tweets = []
        timestamps = []
        usernames = []
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        while len(tweets) < num_tweets:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            
            # Get tweets
            tweet_elements = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')
            
            for element in tweet_elements:
                try:
                    # Get tweet text
                    tweet_text = element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
                    
                    # Get username
                    username = element.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"]').text
                    
                    # Get timestamp
                    timestamp = element.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                    
                    if tweet_text and tweet_text not in tweets:
                        tweets.append(tweet_text)
                        usernames.append(username)
                        timestamps.append(timestamp)
                        
                        if len(tweets) >= num_tweets:
                            break
                except:
                    continue
            
            # Check if we've reached the bottom
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        return tweets[:num_tweets], usernames[:num_tweets], timestamps[:num_tweets]
    
    except Exception as e:
        print(f"Error fetching tweets: {str(e)}")
        return [], [], []

def analyze_sentiment(tweets, usernames, timestamps):
    """Analyze sentiment of tweets"""
    results = []
    for tweet, username, timestamp in zip(tweets, usernames, timestamps):
        blob = TextBlob(tweet)
        sentiment_score = blob.sentiment.polarity
        
        if sentiment_score > 0:
            sentiment = 'Positive'
        elif sentiment_score < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
            
        results.append({
            'timestamp': timestamp,
            'username': username,
            'tweet': tweet,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'subjectivity': blob.sentiment.subjectivity
        })
    
    return pd.DataFrame(results)

def generate_visualizations(df, save_path='twitter_visualizations'):
    """Generate sentiment analysis visualizations"""
    # Create directory for visualizations
    os.makedirs(save_path, exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 1. Sentiment Distribution
    plt.figure(figsize=(10, 6))
    sentiment_counts = df['sentiment'].value_counts()
    plt.bar(sentiment_counts.index, sentiment_counts.values, color=['green', 'red', 'blue'])
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.savefig(f'{save_path}/sentiment_distribution_{current_time}.png')
    plt.close()
    
    # 2. Sentiment Scores Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['sentiment_score'], bins=20, color='skyblue')
    plt.title('Sentiment Scores Distribution')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Count')
    plt.savefig(f'{save_path}/sentiment_scores_distribution_{current_time}.png')
    plt.close() 
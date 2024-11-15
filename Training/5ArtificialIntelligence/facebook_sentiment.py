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
    service = Service()  # If chromedriver is in PATH
    # Or specify path: Service(r'path_to_chromedriver.exe')
    
    # Create driver with service and options
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_comments(driver, url, num_comments=100):
    """Fetch comments from the post"""
    try:
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        
        comments = []
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        while len(comments) < num_comments:
            # Scroll down
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            
            # Get comments
            comment_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='comment-content']")
            
            for element in comment_elements:
                try:
                    comment_text = element.text
                    if comment_text and comment_text not in comments:
                        comments.append(comment_text)
                        if len(comments) >= num_comments:
                            break
                except:
                    continue
            
            # Check if we've reached the bottom
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        return comments[:num_comments]
    
    except Exception as e:
        print(f"Error fetching comments: {str(e)}")
        return []

def analyze_sentiment(comments):
    """Analyze sentiment of comments"""
    results = []
    for comment in comments:
        blob = TextBlob(comment)
        sentiment_score = blob.sentiment.polarity
        
        if sentiment_score > 0:
            sentiment = 'Positive'
        elif sentiment_score < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
            
        results.append({
            'comment': comment,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'subjectivity': blob.sentiment.subjectivity
        })
    
    return pd.DataFrame(results)

def generate_visualizations(df):
    """Generate sentiment analysis visualizations"""
    # Sentiment Distribution
    plt.figure(figsize=(10, 6))
    df['sentiment'].value_counts().plot(kind='bar')
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()
    
    # Sentiment Scores Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['sentiment_score'], bins=20)
    plt.title('Sentiment Scores Distribution')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()
    
    # Subjectivity Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['subjectivity'], bins=20)
    plt.title('Subjectivity Distribution')
    plt.xlabel('Subjectivity Score')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def main():
    # Facebook post URL
    post_url = "YOUR_FACEBOOK_POST_URL"
    
    print("Starting Facebook comment analysis...")
    
    # Setup driver
    driver = setup_driver()
    
    try:
        # Initial
        print("Fetching initial 100 comments...")
        comments = fetch_comments(driver, post_url, 100)
        print(f"Fetched {len(comments)} comments")
        
        if comments:
            # Analyze sentiment
            df = analyze_sentiment(comments)
            
            # Save to CSV
            df.to_csv('facebook_comments_analysis.csv', index=False)
            print("Analysis saved to facebook_comments_analysis.csv")
            
            # Generate visualizations
            generate_visualizations(df)
            
            # Print summary
            print("\nSentiment Analysis Summary:")
            print(df['sentiment'].value_counts())
            print("\nAverage Sentiment Score:", df['sentiment_score'].mean())
            
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
    
    finally:
        driver.quit()

if __name__ == '__main__':
    main()

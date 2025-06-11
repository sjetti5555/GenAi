from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
from textblob import TextBlob
import time

# Set the path to the ChromeDriver executable
chrome_driver_path = r"C:\\Users\\srira\\Downloads\\chromedriver-win64\\chromedriver.exe"  # Use raw string for the path

# Set up Chrome options to disable GPU acceleration
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--headless")  # Run in headless mode (optional)

# Set up the Selenium WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Maximize the browser window
driver.maximize_window()

# Define the URL of the YouTube video comments page
url = 'https://www.youtube.com/watch?v=SGUP6BkA870'  # Replace with your desired video URL
driver.get(url)  # Navigate to the URL

# Wait for the comments section to load
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ytd-comments'))
    )
except Exception as e:
    print("Error loading comments section:", e)

# Wait a bit to ensure comments are fully loaded
time.sleep(5)  # Adjust the sleep time as necessary

# Scroll down to load more comments (optional)
for _ in range(3):  # Adjust the range for more scrolling
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)  # Wait for comments to load

# Find all the comments and usernames on the page
comments = driver.find_elements(By.CSS_SELECTOR, 'span.yt-core-attributed-string')
usernames = driver.find_elements(By.CSS_SELECTOR, 'span.style-scope.ytd-comment-view-model')

# Create a list to store the comments and usernames
comment_list = []
username_list = []

# Loop through each comment and extract the text and username
for comment, username in zip(comments, usernames):
    comment_text = comment.text
    username_text = username.text.strip()  # Remove any leading/trailing whitespace
    comment_list.append(comment_text)
    username_list.append(username_text)

    # Stop after collecting 100 comments
    if len(comment_list) >= 100:
        break

# Debugging: Print the number of comments and usernames collected
print(f"Collected {len(comment_list)} comments and {len(username_list)} usernames.")

# Check if any comments were collected
if not comment_list or not username_list:
    print("No comments or usernames were collected. Please check the CSS selectors and page loading.")
else:
    # Create a DataFrame to store the comments, usernames, and their sentiment
    df = pd.DataFrame({
        'username': username_list,
        'comment': comment_list
    })

    # Analyze the sentiment of each comment
    df['polarity'] = df['comment'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment'] = np.where(df['polarity'] > 0, 'positive', np.where(df['polarity'] < 0, 'negative', 'neutral'))

    # Save the DataFrame to a CSV file
    df.to_csv('data/comments_sentiment.csv', index=False)

    # Print the DataFrame to see the output
    print("Sentiment analysis results saved to 'data/comments_sentiment.csv':")
    print(df)

# Close the browser
driver.quit()

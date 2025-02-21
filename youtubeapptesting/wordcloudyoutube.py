import re
from googleapiclient.discovery import build
from langdetect import detect
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# Fetch All Comments Using Pagination
def fetch_comments(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []
    next_page_token = None

    while True:
        try:
            # Request comments with pagination
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token  # Get the next page of comments
            )
            response = request.execute()

            # Extract comments
            for item in response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # Check if there's another page of comments
            next_page_token = response.get('nextPageToken')
            if not next_page_token:  # No more pages
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return comments


# Detect Language Dynamically with Transliterated Telugu Handling
def detect_language(comment):
    clean_text = clean_comment(comment)
    try:
        lang = detect(clean_text)
        if lang == "te":
            return "Telugu"
        elif lang == "en":
            if re.search(r"[\u0C00-\u0C7F]", comment):  # Contains Telugu characters
                return "Mixed"
            else:
                return "English"
        else:
            return "Mixed"  # Mixed or Unknown
    except:
        return "Telugu (Transliterated)"  # If langdetect fails, assume Transliterated Telugu

# Clean and Preprocess Comments
def clean_comment(comment):
    # Remove special characters, links, and extra spaces
    comment = re.sub(r"http\S+|www\S+|https\S+", '', comment, flags=re.MULTILINE)
    comment = re.sub(r"[^a-zA-Z0-9\u0C00-\u0C7F\s]", '', comment)  # Keep Telugu and English characters
    return comment.strip()

# Generate Word Cloud
def generate_wordcloud(text, title):
    wordcloud = WordCloud(
        width=1600, height=800,
        background_color='white',
        max_words=1000,
        collocations=False
    ).generate(text)

    plt.figure(figsize=(14, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title, fontsize=18)
    plt.axis('off')
    plt.show()

# Main Script
if __name__ == "__main__":
    API_KEY = "Youtube_Api_key"
    video_link = input("Enter YouTube video link: ").strip()
    video_id = re.search(r"v=([^&]+)", video_link).group(1) if "v=" in video_link else None

    if not video_id:
        print("Invalid video link. Please provide a valid YouTube URL.")
    else:
        print(f"Fetching comments for video ID: {video_id}")
        comments = fetch_comments(video_id, API_KEY)

        if comments:
            print(f"Total comments fetched: {len(comments)}")

            # Categorize Comments by Language
            telugu_comments = []
            transliterated_telugu_comments = []
            english_comments = []
            mixed_comments = []

            for comment in comments:
                language = detect_language(comment)
                if language == "Telugu":
                    telugu_comments.append(comment)
                elif language == "Telugu (Transliterated)":
                    transliterated_telugu_comments.append(comment)
                elif language == "English":
                    english_comments.append(comment)
                else:
                    mixed_comments.append(comment)

            # Save Comments to CSV
            print("Saving categorized comments to CSV...")
            df = pd.DataFrame({
                "Comment": comments,
                "Language": [detect_language(c) for c in comments]
            })
            df.to_csv("categorized_comments.csv", index=False)
            print("Categorized comments saved to 'categorized_comments.csv'.")

            # Generate Word Clouds
            if english_comments:
             print("Generating Word Cloud for English Comments...")
             generate_wordcloud(" ".join(english_comments), "English Comments Word Cloud")

            if mixed_comments:
             print("Generating Word Cloud for Mixed Comments...")
            generate_wordcloud(" ".join(mixed_comments), "Mixed Comments Word Cloud")


        else:
            print("No comments available for analysis.")

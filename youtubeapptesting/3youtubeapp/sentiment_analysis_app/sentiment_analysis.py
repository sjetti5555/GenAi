import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import pipeline
from youtube_scraper import get_video_comments

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def clean_text(text):
    """Clean and preprocess text data."""
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"https?://\S+|www\.\S+", "", text)
    text = re.sub(r"[^A-Za-z0-9 ]+", "", text)
    tokens = word_tokenize(text)
    return " ".join(word for word in tokens if word not in stopwords.words("english"))

def get_sentiment(text):
    """Analyze sentiment of a given text."""
    try:
        cleaned_text = clean_text(text)
        result = sentiment_analyzer(cleaned_text)[0]
        return {"label": result["label"], "score": round(result["score"], 2)}
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {"label": "Unknown", "score": 0.0}

def analyze_video(video_id):
    """Perform overall sentiment analysis for a video."""
    comments = get_video_comments(video_id)
    if not comments:
        return {
            "overall_sentiment": "No comments",
            "average_score": 0.0,
            "total_comments": 0,
            "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
        }

    total_score = 0
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

    for comment in comments:
        sentiment = get_sentiment(comment["text"])
        total_score += sentiment["score"]

        if sentiment["label"].lower() in ["1 star", "2 stars"]:
            sentiment_counts["negative"] += 1
        elif sentiment["label"].lower() in ["3 stars"]:
            sentiment_counts["neutral"] += 1
        elif sentiment["label"].lower() in ["4 stars", "5 stars"]:
            sentiment_counts["positive"] += 1

    total_comments = len(comments)
    average_score = total_score / total_comments if total_comments > 0 else 0.0

    overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)

    return {
        "overall_sentiment": overall_sentiment,
        "average_score": round(average_score, 2),
        "total_comments": total_comments,
        "sentiment_distribution": sentiment_counts,
    }

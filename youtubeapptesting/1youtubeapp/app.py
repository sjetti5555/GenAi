import os
from flask import Flask, request, jsonify, render_template
from googleapiclient.discovery import build
from transformers import pipeline, AutoTokenizer, TFAutoModelForSequenceClassification
import threading
import time
from collections import Counter
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Initialize Flask app
app = Flask(__name__)

# YouTube API Configuration
# The API key should be provided via the ``YOUTUBE_API_KEY`` environment variable
API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Sentiment Analysis Model - TensorFlow Implementation
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, framework="tf")

# Global variables for monitoring comments
MONITORED_COMMENTS = {}
MONITOR_INTERVAL = 30 * 60  # 30 minutes

# Fetch YouTube Comments
def fetch_youtube_comments(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    comments_data = []
    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=20,  # Limit to 20 comments for faster execution
            textFormat='plainText'
        )
        while request:
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                author_name = item['snippet']['topLevelComment']['snippet'].get('authorDisplayName', 'Anonymous')
                channel_id = item['snippet']['topLevelComment']['snippet'].get('authorChannelId', {}).get('value', 'Unknown')
                comments_data.append({'comment': comment, 'author': author_name, 'channel_id': channel_id})
            request = youtube.commentThreads().list_next(request, response)
    except Exception as e:
        print(f"Error fetching comments: {e}")
    return comments_data

# Analyze Sentiments
def analyze_sentiments(comments_data):
    results = []
    sentiment_counts = Counter()
    
    for data in comments_data:
        try:
            sentiment = sentiment_analyzer(data['comment'])[0]
            sentiment_label = sentiment['label']
            confidence = sentiment['score']

            if sentiment_label in ["1 star", "2 stars"]:
                overall_sentiment = "NEGATIVE"
            elif sentiment_label == "3 stars":
                overall_sentiment = "NEUTRAL"
            elif sentiment_label in ["4 stars", "5 stars"]:
                overall_sentiment = "POSITIVE"
            else:
                overall_sentiment = "UNKNOWN"

            sentiment_counts[overall_sentiment] += 1

            results.append({
                'comment': data['comment'],
                'author': data['author'],
                'channel_id': data['channel_id'],
                'sentiment': overall_sentiment,
                'confidence': round(confidence, 2)
            })
        except Exception as e:
            print(f"Error analyzing comment: {data['comment']} | {e}")
            results.append({
                'comment': data['comment'],
                'author': data['author'],
                'channel_id': data['channel_id'],
                'sentiment': 'Error',
                'confidence': 0
            })

    # Determine overall sentiment based on counts
    total_comments = sum(sentiment_counts.values())
    if total_comments == 0:
        overall_sentiment = "UNKNOWN"
    else:
        overall_sentiment = sentiment_counts.most_common(1)[0][0]

    return results, sentiment_counts, overall_sentiment

# Generate Graph
def generate_graph(sentiment_counts):
    labels = sentiment_counts.keys()
    sizes = sentiment_counts.values()
    colors = ['#ff9999', '#66b3ff', '#99ff99']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode()
    buf.close()
    return graph_url

# Monitor New Comments
def monitor_comments(video_id):
    global MONITORED_COMMENTS
    while True:
        new_comments = fetch_youtube_comments(video_id)
        new_comments = [c for c in new_comments if c['comment'] not in MONITORED_COMMENTS]

        if new_comments:
            print(f"New comments detected: {len(new_comments)}")
            MONITORED_COMMENTS.update({c['comment']: True for c in new_comments})

        time.sleep(MONITOR_INTERVAL)

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Analyze Route
@app.route('/analyze', methods=['POST'])
def analyze():
    video_url = request.form['video_url']
    if "v=" not in video_url:
        return jsonify({'error': 'Invalid YouTube URL'})
    video_id = video_url.split("v=")[-1]

    # Start monitoring new comments
    global MONITORED_COMMENTS
    threading.Thread(target=monitor_comments, args=(video_id,), daemon=True).start()

    comments_data = fetch_youtube_comments(video_id)
    if not comments_data:
        return jsonify({'error': 'No comments found or invalid video ID'})

    MONITORED_COMMENTS.update({c['comment']: True for c in comments_data})

    sentiment_results, sentiment_counts, overall_sentiment = analyze_sentiments(comments_data)
    graph_url = generate_graph(sentiment_counts)

    return jsonify({
        'results': sentiment_results,
        'positive_count': sentiment_counts['POSITIVE'],
        'negative_count': sentiment_counts['NEGATIVE'],
        'neutral_count': sentiment_counts['NEUTRAL'],
        'overall_sentiment': overall_sentiment,
        'graph_url': f"data:image/png;base64,{graph_url}"
    })

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

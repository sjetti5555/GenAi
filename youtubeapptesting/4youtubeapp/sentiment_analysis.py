import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import pipeline
from langdetect import detect, LangDetectException

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9 ]+', '', text)
    tokens = word_tokenize(text)
    return ' '.join(word for word in tokens if word not in stopwords.words('english'))

def get_sentiment(text):
    try:
        if detect(text) != 'en':
            return None, None
        result = sentiment_analyzer(text)[0]
        return result['label'], round(result['score'], 2)
    except LangDetectException:
        return None, None

import streamlit as st
import requests
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --------------------------
# Utility Functions
# --------------------------

def fetch_news(company, api_key):
    """Fetch latest news articles about the company using NewsData.io"""
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={company}&language=en"
    try:
        response = requests.get(url)
        data = response.json()
        if "results" in data:
            return [article["title"] + " " + article.get("description", "") for article in data["results"]]
    except Exception as e:
        st.error(f"Error fetching news: {e}")
    return []

def fetch_culture_snippets(company):
    """Load from sample reviews (fake Glassdoor-like data for prototype)"""
    try:
        with open("sample_reviews.json", "r") as f:
            reviews = json.load(f)
        return reviews.get(company, [])
    except Exception:
        return []

def generate_wordcloud(text):
    """Generate and plot a word cloud"""
    if not text.strip():
        return None
    wordcloud = WordCloud(width=800, height=400, background_color="white", collocations=False).generate(text)
    return wordcloud

def analyze_sentiment(texts):
    """Simple sentiment polarity analysis using TextBlob"""
    if not texts:
        return "Not enough data"
    polarity = sum(TextBlob(t).sentiment.polarity for t in texts) / len(texts)
    if polarity > 0.1:
        return "Overall Positive Sentiment 😊"
    elif polarity < -0.1:
        return "Overall Negative Sentiment 😟"
    else:
        return "Mixed/Neutral Sentiment 😐"

def create_pdf(company, news, culture, sentiment):
    """Generate PDF report and return as BytesIO"""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"HR Due Diligence Report: {company}")

    y = height - 100
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "📈 Sentiment Summary:")
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(60,

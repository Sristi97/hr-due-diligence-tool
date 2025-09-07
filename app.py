# app.py
import os
import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob

st.set_page_config(page_title="HR Due Diligence Tool", layout="centered")

# Fetch API key from CloudStream Secrets
NEWS_API_KEY = os.environ.get("NEWSDATA_API_KEY")

if not NEWS_API_KEY:
    st.error("API key not set! Please add it in CloudStream Secrets.")
    st.stop()

st.title("HR Due Diligence Tool")
st.write("Fetch news, culture, reputation, and insights about companies for HR due diligence.")

company_name = st.text_input("Enter Company Name", "")

def fetch_news(company):
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWS_API_KEY,
        "q": company,
        "language": "en"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "results" in data and data["results"]:
            return [{"title": r.get("title"), "link": r.get("link"), "pubDate": r.get("pubDate"), "description": r.get("description")} for r in data["results"]]
        else:
            return []
    except Exception as e:
        st.warning(f"Error fetching news: {e}")
        return []

def fetch_google_snippets(company):
    # Placeholder: replace with real API if available
    return [{"snippet": f"No snippet data available for {company}"}]

def analyze_sentiment(news_list):
    # Simple sentiment: +1 positive, -1 negative based on title/description
    score = 0
    text_corpus = ""
    for item in news_list:
        content = (item.get("title") or "") + " " + (item.get("description") or "")
        text_corpus += " " + content
        polarity = TextBlob(content).sentiment.polarity
        if polarity > 0.1:
            score += 1
        elif polarity < -0.1:
            score -= 1
    # Normalize score to 0-100 scale
    max_score = len(news_list) if news_list else 1
    reputation = int((score + max_score) / (2 * max_score) * 100)
    return reputation, text_corpus

def generate_wordcloud(text):
    if not text.strip():
        return None
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    return wc

if company_name:
    st.subheader(f"Fetching info for {company_name}...")

    news_results = fetch_news(company_name)
    google_results = fetch_google_snippets(company_name)
    
    reputation, corpus = analyze_sentiment(news_results)
    wordcloud_img = generate_wordcloud(corpus)

    # JSON result
    results = {
        "company": company_name,
        "news": news_results,
        "google_snippets": google_results,
        "reputation_score": reputation
    }

    st.json(results)

    # Display Word Cloud
    if wordcloud_img:
        st.subheader("Word Cloud from news")
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud_img, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

    if not news_results:
        st.info("No news articles found.")
    if not google_results or google_results == [{"snippet": f"No snippet data available for {company_name}"}]:
        st.info("No Google snippet info available.")

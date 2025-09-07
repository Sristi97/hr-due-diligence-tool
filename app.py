import os
import json
import requests
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ----------------------------
# Config
# ----------------------------
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")

st.title("HR Due Diligence Dashboard")
company_name = st.text_input("Enter company name", "Reliance")

API_KEY = os.getenv("NEWSDATA_API_KEY")  # CloudStream secret

# ----------------------------
# Helper Functions
# ----------------------------

def fetch_news(company):
    """Fetch news from NewsData API"""
    if not API_KEY:
        return {"error": "API key not set", "data": []}
    try:
        response = requests.get(
            f"https://newsdata.io/api/1/news?apikey={API_KEY}&q={company}&page=1"
        )
        if response.status_code != 200:
            return {"error": f"API returned status {response.status_code}", "data": []}
        result = response.json()
        if result.get("status") != "success" or not result.get("results"):
            return {"error": "No news found", "data": []}
        news_items = [
            {"title": n.get("title"), "link": n.get("link"), "pubDate": n.get("pubDate")}
            for n in result.get("results", [])
        ]
        return {"error": None, "data": news_items}
    except Exception as e:
        return {"error": str(e), "data": []}

def load_dummy_data():
    """Load fallback dummy data"""
    with open("sample_reviews.json", "r") as f:
        return json.load(f)

def generate_wordcloud(text_list):
    """Create a word cloud from a list of text"""
    text = " ".join(text_list)
    if not text.strip():
        return None
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    return wc

# ----------------------------
# Main Logic
# ----------------------------

if company_name:
    st.header(f"Company: {company_name}")

    # Try fetching news, fallback to dummy
    news_data = fetch_news(company_name)
    if not news_data["data"]:
        st.warning("News API unavailable, using sample data.")
        data = load_dummy_data()
        news_data = data["news"]
        google_data = data["google_snippets"]
        reputation_data = data["reputation"]
    else:
        google_data = load_dummy_data()["google_snippets"]
        reputation_data = load_dummy_data()["reputation"]

    # Display News
    st.subheader("Latest News")
    if news_data["data"]:
        for n in news_data["data"]:
            st.markdown(f"- [{n['title']}]({n['link']}) ({n['pubDate']})")
    else:
        st.info("No news available.")

    # Display Google snippets
    st.subheader("Google Snippets / Culture Insights")
    for snippet in google_data.get("data", []):
        st.markdown(f"- {snippet}")

    # Display Reputation
    st.subheader("Employee Reputation / Reviews")
    for key, section in reputation_data.items():
        st.markdown(f"**{key.capitalize()}**")
        for item in section.get("data", []):
            st.markdown(f"- {item}")

    # Generate Word Cloud
    st.subheader("Culture / Sentiment Word Cloud")
    word_texts = google_data.get("data", []) + reputation_data.get("reviews", {}).get("data", [])
    wc = generate_wordcloud(word_texts)
    if wc:
        plt.figure(figsize=(12,6))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.info("No text available for word cloud.")

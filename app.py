import streamlit as st
import json
import requests

st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

# Input for company
company = st.text_input("Enter Company Name", "Reliance")

# Load fallback JSON data
with open("sample_reviews.json") as f:
    fallback_data = json.load(f)

# --- Fetch news from NewsData.io ---
news_data = []
try:
    API_KEY = st.secrets["NEWSDATA_API_KEY"]
    resp = requests.get(f"https://newsdata.io/api/1/news?apikey={API_KEY}&q={company}")
    data = resp.json()
    if data.get("status") == "success" and data.get("results"):
        news_data = data.get("results")
    else:
        news_data = fallback_data["news"]["data"]
except:
    news_data = fallback_data["news"]["data"]

# Culture / Sentiment
culture_snippets = fallback_data.get("google_snippets", [])
wordcloud_words = fallback_data.get("culture_wordcloud", [])

# Reputation / Reviews
reputation = fallback_data.get("reputation", {})

# --- Display sections ---
st.subheader("News")
for n in news_data:
    st.markdown(f"- {n.get('title','No title')} ({n.get('pubDate','')})")

st.subheader("Culture / Sentiment Word Cloud")
st.text(" | ".join(wordcloud_words))
st.text("Highlights: " + " | ".join(culture_snippets))

st.subheader("Employee Reputation / Reviews")
st.json(reputation)

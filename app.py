import os
import json
import requests
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -----------------------
# App Config
# -----------------------
st.set_page_config(page_title="HR Due Diligence Tool", layout="wide")
st.title("HR Due Diligence Dashboard")

# -----------------------
# Inputs
# -----------------------
company_name = st.text_input("Enter Company Name", "Reliance")

# -----------------------
# Load API Key & Fallback JSON
# -----------------------
NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")
fallback_file = "sample_reviews.json"

try:
    with open(fallback_file, "r") as f:
        fallback_data = json.load(f)
except Exception:
    fallback_data = {}

# -----------------------
# Fetch News
# -----------------------
news_data = []
if NEWS_API_KEY:
    try:
        url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={company_name}&language=en"
        response = requests.get(url).json()
        if response.get("status") == "success":
            news_data = response.get("results", [])
        else:
            st.warning(f"News API returned an error: {response.get('message', 'Unknown error')}")
    except Exception as e:
        st.error(f"Error fetching news: {e}")
else:
    st.info("NEWS API key not set. Using fallback data.")

# -----------------------
# Fallback News
# -----------------------
if not news_data:
    news_data = fallback_data.get("news", {}).get("data", [])
    if news_data:
        st.info("Using sample JSON news data.")
    else:
        st.warning("No news available in fallback JSON.")

# -----------------------
# Fetch Google Snippets / Reputation
# -----------------------
google_snippets = fallback_data.get("google_snippets", {}).get(company_name, {"message": "No Google snippets found."})
reputation = fallback_data.get("reputation", {}).get(company_name, {
    "reviews": {"message": "No reviews found."},
    "employee_satisfaction": {"message": "No employee satisfaction data."},
    "ratings": {"message": "No ratings found."},
    "Glassdoor": {"message": "No Glassdoor data."}
})

# -----------------------
# Word Cloud from Culture / Sentiment
# -----------------------
text_for_wordcloud = ""
for item in news_data:
    text_for_wordcloud += " " + item.get("title", "") + " " + item.get("description", "")

if not text_for_wordcloud.strip():
    # Fallback text
    text_for_wordcloud = "Work culture Employee engagement HR satisfaction Benefits Leadership Teamwork Innovation"

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_for_wordcloud)
st.subheader("Culture / Sentiment Word Cloud")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# -----------------------
# Display JSON Data
# -----------------------
st.subheader("Raw JSON Data")
output_json = {
    "company": company_name,
    "news": news_data if news_data else {"message": "No news available."},
    "google_snippets": google_snippets,
    "reputation": reputation
}
st.json(output_json)

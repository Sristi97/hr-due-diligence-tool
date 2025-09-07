import streamlit as st
import requests
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob

# -----------------------------
# Function: Fetch news articles from NewsData.io
# -----------------------------
def fetch_news(company, api_key):
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={company}&language=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("results", [])
        texts = [a.get("title", "") + " " + a.get("description", "") for a in articles if a]
        return texts
    else:
        return []

# -----------------------------
# Function: Sentiment Analysis
# -----------------------------
def analyze_sentiment(texts):
    sentiments = [TextBlob(t).sentiment.polarity for t in texts if t.strip()]
    if not sentiments:
        return 0, "Neutral"
    avg = sum(sentiments) / len(sentiments)
    if avg > 0.1:
        return avg, "Positive"
    elif avg < -0.1:
        return avg, "Negative"
    else:
        return avg, "Neutral"

# -----------------------------
# Function: Load sample employee reviews
# -----------------------------
def load_reviews():
    try:
        with open("sample_reviews.json", "r") as f:
            reviews = json.load(f)
        return reviews
    except:
        return []

# -----------------------------
# Function: Fetch jobs (placeholder sample data)
# -----------------------------
def fetch_jobs(company):
    jobs = [
        {"title": "HR Business Partner", "location": "Mumbai", "type": "Full-time"},
        {"title": "Software Engineer", "location": "Bangalore", "type": "Full-time"},
        {"title": "Talent Acquisition Specialist", "location": "Hyderabad", "type": "Contract"},
    ]
    return jobs

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="HR Due Diligence Tool", layout="wide")

st.title("🕵️ HR Due Diligence Dashboard")
st.markdown("Prototype tool to analyze **company culture, hiring trends, and reputation** using open data sources.")

# Inputs
company = st.text_input("Enter company name:", "Reliance Industries")
api_key = st.text_input("Enter your NewsData.io API Key", type="password")

if st.button("Run Analysis"):
    col1, col2, col3 = st.columns(3)

    # --- Culture & Reviews ---
    with col1:
        st.subheader("💬 Culture & Reviews")
        reviews = load_reviews()
        if reviews:
            for r in reviews[:3]:  # show top 3 reviews
                with st.container():
                    st.markdown(f"**{r['review']}**")
                    st.markdown(f"- 👍 {r['pros']}")
                    st.markdown(f"- 👎 {r['cons']}")
                    st.markdown("---")
        else:
            st.warning("No reviews available (sample only).")

    # --- Jobs & Hiring Trends ---
    with col2:
        st.subheader("📈 Jobs & Hiring Trends")
        jobs = fetch_jobs(company)
        if jobs:
            for j in jobs[:3]:  # top 3 jobs
                with st.container():
                    st.markdown(f"**{j['title']}**")
                    st.markdown(f"📍 {j['location']} — {j['type']}")
                    st.markdown("---")
        else:
            st.warning("No jobs found.")

    # --- Reputation & News ---
    with col3:
        st.subheader("📰 Reputation & News")
        if not api_key:
            st.error("Enter your NewsData.io API key.")
        else:
            news_texts = fetch_news(company, api_key)
            if news_texts:
                combined_text = " ".join(news_texts)

                # Sentiment
                avg_score, sentiment = analyze_sentiment(news_texts)
                st.markdown(f"**Sentiment:** {sentiment} ({avg_score:.2f})")

                # Word Cloud
                wordcloud = WordCloud(width=400, height=200, background_color="white").generate(combined_text)
                fig, ax = plt.subplots(figsize=(5, 3))
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)

                # Show headlines
                st.markdown("**Top News:**")
                for i, text in enumerate(news_texts[:3], 1):
                    st.write(f"{i}. {text}")
            else:
                st.warning("No news found.")

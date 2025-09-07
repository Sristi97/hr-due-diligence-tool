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
# Function: Load sample employee reviews (simulate Glassdoor)
# -----------------------------
def load_reviews():
    try:
        with open("sample_reviews.json", "r") as f:
            reviews = json.load(f)
        return reviews
    except:
        return []

# -----------------------------
# Function: Fetch jobs from Jooble (free jobs API)
# -----------------------------
def fetch_jobs(company):
    # Sample placeholder (since Jooble/Adzuna require signup + free keys)
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

st.title("🕵️ HR Due Diligence Analysis Dashboard")
st.markdown("A prototype tool to analyze company culture, jobs, and reputation using open data sources.")

# Inputs
company = st.text_input("Enter company name:", "Reliance Industries")
api_key = st.text_input("Enter your NewsData.io API Key", type="password")

if st.button("Run Analysis"):
    # --- Section 1: Employee Reviews ---
    st.header("💬 Culture & Employee Reviews")
    reviews = load_reviews()
    if reviews:
        for r in reviews[:5]:  # show top 5 reviews
            st.markdown(f"**Review:** {r['review']}")
            st.markdown(f"- 👍 Pros: {r['pros']}")
            st.markdown(f"- 👎 Cons: {r['cons']}")
            st.markdown("---")
    else:
        st.warning("No reviews available (using sample data only).")

    # --- Section 2: Jobs & Hiring Trends ---
    st.header("📈 Jobs & Hiring Trends")
    jobs = fetch_jobs(company)
    if jobs:
        for j in jobs:
            st.markdown(f"**{j['title']}** – {j['location']} ({j['type']})")
    else:
        st.warning("No jobs found.")

    # --- Section 3: Reputation & Compliance (News) ---
    st.header("📰 Reputation & Compliance (News Analysis)")
    if not api_key:
        st.error("Please enter your NewsData.io API key for news analysis.")
    else:
        news_texts = fetch_news(company, api_key)
        if news_texts:
            combined_text = " ".join(news_texts)

            # Sentiment
            avg_score, sentiment = analyze_sentiment(news_texts)
            st.markdown(f"**Overall News Sentiment:** {sentiment} ({avg_score:.2f})")

            # Word Cloud
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(combined_text)
            st.subheader("Word Cloud from News Mentions")
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

            # Articles
            st.subheader("Latest News Articles")
            for i, text in enumerate(news_texts[:5], 1):  # show top 5
                st.write(f"**{i}.** {text}")
        else:
            st.warning("No news found for this company.")

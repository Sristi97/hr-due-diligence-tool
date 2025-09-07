import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob

# -----------------------------
# Function to fetch news from NewsData.io
# -----------------------------
def fetch_news(company, api_key):
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={company}&language=en"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("results", [])
        texts = [a.get("title", "") + " " + a.get("description", "") for a in articles if a]
        return texts, articles
    else:
        return [], []

# -----------------------------
# Function for sentiment analysis
# -----------------------------
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# -----------------------------
# Streamlit App
# -----------------------------
st.title("🕵️ HR Due Diligence Company Analysis Tool")

# User inputs
company = st.text_input("Enter company name:", "Reliance Industries")
api_key = st.text_input("Enter your NewsData.io API Key", type="password")

if st.button("Fetch & Analyze"):
    if not api_key:
        st.error("Please enter your NewsData.io API key.")
    else:
        st.info(f"Fetching latest news for: {company} ...")
        news_texts, articles = fetch_news(company, api_key)

        if news_texts:
            combined_text = " ".join(news_texts)

            # Word Cloud
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)

            st.subheader("Word Cloud of Company Mentions")
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

            # Sentiment Summary
            sentiments = [analyze_sentiment(text) for text in news_texts]
            pos = sentiments.count("Positive")
            neg = sentiments.count("Negative")
            neu = sentiments.count("Neutral")

            st.subheader("📊 Sentiment Analysis Summary")
            st.write(f"✅ Positive: {pos}")
            st.write(f"⚠️ Negative: {neg}")
            st.write(f"➖ Neutral: {neu}")

            # Show Articles with Sentiment
            st.subheader("📰 Latest News Articles with Sentiment")
            for i, article in enumerate(articles[:10], 1):  # show top 10
                title = article.get("title", "No Title")
                description = article.get("description", "")
                link = article.get("link", "#")
                sentiment = analyze_sentiment(title + " " + description)
                st.markdown(f"**{i}. [{title}]({link})**  \nSentiment: **{sentiment}**  \n{description}")

        else:
            st.warning("No news found. Try another company name or check your API key.")

import streamlit as st
import requests
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -----------------------------
# Replace with your NewsAPI.org key
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"
# -----------------------------

# Function to fetch news articles about the company
def fetch_news(company_name):
    url = "https://newsapi.org/v2/everything"
    query = f"{company_name} employee OR culture OR workplace OR attrition"
    params = {
        "q": query,
        "language": "en",
        "pageSize": 10,  # number of articles
        "apiKey": NEWS_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        news_texts = [article.get('description', '') for article in data.get('articles', []) if article.get('description')]
        return news_texts
    except:
        return []

# ----------------------------- Streamlit UI -----------------------------
st.title("HR Due Diligence Tool - Live Data (NewsAPI.org)")

company_name = st.text_input("Enter company name:")

if company_name:
    # ----------------- Fetch News -----------------
    news_texts = fetch_news(company_name)
    
    st.subheader("Fetched News Articles")
    if news_texts:
        for idx, article in enumerate(news_texts, 1):
            st.write(f"{idx}. {article}")
    else:
        st.write("No news articles found.")

    # ----------------- Combine Text for Analysis -----------------
    combined_text = " ".join(news_texts)

    if combined_text.strip():  # Only process if there is text
        # ----------------- Sentiment Analysis -----------------
        sentiment_score = TextBlob(combined_text).sentiment.polarity
        st.subheader("Overall Sentiment Score")
        st.write(sentiment_score)

        # ----------------- Word Cloud -----------------
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # ----------------- Downloadable Report -----------------
        report_text = f"Company: {company_name}\n\nSentiment Score: {sentiment_score}\n\nNews Articles:\n"
        report_text += "\n".join(news_texts)
        st.download_button("Download Report", report_text, file_name=f"{company_name}_HR_report.txt")
    else:
        st.write("No news text available. Word cloud and sentiment analysis cannot be generated.")

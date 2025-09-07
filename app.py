import streamlit as st
import requests
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -----------------------------
# Replace with your Bing News API key
NEWS_API_KEY = "YOUR_BING_API_KEY"
# -----------------------------

# Function to fetch news about company culture and reviews
def fetch_news(company_name):
    search_url = "https://api.bing.microsoft.com/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key": NEWS_API_KEY}
    query = f"{company_name} employee reviews OR culture OR workplace OR attrition"
    params = {"q": query, "mkt": "en-US", "count": 10}
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    news_texts = [article.get('description', '') for article in data.get('value', [])]
    return news_texts

# Streamlit app
st.title("HR Due Diligence Tool - Live Data")

company_name = st.text_input("Enter company name:")

if company_name:
    st.subheader("Fetched News Articles")
    news_texts = fetch_news(company_name)
    if news_texts:
        for idx, article in enumerate(news_texts, 1):
            st.write(f"{idx}. {article}")
    else:
        st.write("No news articles found.")

    # Combine all text for sentiment and word cloud
    combined_text = " ".join(news_texts)

    # Sentiment analysis
    sentiment_score = TextBlob(combined_text).sentiment.polarity
    st.subheader("Overall Sentiment Score")
    st.write(sentiment_score)

    # Word cloud generation
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Downloadable report
    report_text = f"Company: {company_name}\n\nSentiment Score: {sentiment_score}\n\nNews Articles:\n"
    report_text += "\n".join(news_texts)
    st.download_button("Download Report", report_text, file_name=f"{company_name}_HR_report.txt")

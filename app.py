import streamlit as st
import requests
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tweepy

# -----------------------------
# Replace with your Bing News API key
NEWS_API_KEY = "YOUR_BING_API_KEY"

# Replace with your Twitter API credentials
TWITTER_BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"
# -----------------------------

# Function to fetch news articles about the company
def fetch_news(company_name):
    search_url = "https://api.bing.microsoft.com/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key": NEWS_API_KEY}
    query = f"{company_name} employee reviews OR culture OR workplace OR attrition"
    params = {"q": query, "mkt": "en-US", "count": 10}
    response = requests.get(search_url, headers=headers, params=params)
    data = response.json()
    news_texts = [article.get('description', '') for article in data.get('value', [])]
    return news_texts

# Function to fetch tweets about the company
def fetch_tweets(company_name):
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
    query = f"{company_name} employee OR culture OR workplace -is:retweet lang:en"
    tweets = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['text'])
    tweet_texts = [tweet.text for tweet in tweets.data] if tweets.data else []
    return tweet_texts

# Streamlit app
st.title("HR Due Diligence Tool - Live Data (News + Twitter)")

company_name = st.text_input("Enter company name:")

if company_name:
    # ----------------- News -----------------
    st.subheader("Fetched News Articles")
    news_texts = fetch_news(company_name)
    if news_texts:
        for idx, article in enumerate(news_texts, 1):
            st.write(f"{idx}. {article}")
    else:
        st.write("No news articles found.")

    # ----------------- Tweets -----------------
    st.subheader("Recent Tweets")
    tweet_texts = fetch_tweets(company_name)
    if tweet_texts:
        for idx, tweet in enumerate(tweet_texts, 1):
            st.write(f"{idx}. {tweet}")
    else:
        st.write("No tweets found.")

    # Combine all text for sentiment and word cloud
    combined_text = " ".join(news_texts + tweet_texts)

    # Sentiment analysis
    sentiment_score = TextBlob(combined_text).sentiment.polarity
    st.subheader("Overall Sentiment Score")
    st.write(sentiment_score)

    # Word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Downloadable report
    report_text = f"Company: {company_name}\n\nSentiment Score: {sentiment_score}\n\nNews Articles:\n"
    report_text += "\n".join(news_texts)
    report_text += "\n\nTweets:\n" + "\n".join(tweet_texts)
    st.download_button("Download Report", report_text, file_name=f"{company_name}_HR_report.txt")

import streamlit as st
import wikipedia
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

# NewsAPI key
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"  # Replace with your key

# Function to fetch Wikipedia summary
def fetch_wiki_summary(company_name):
    try:
        summary = wikipedia.summary(company_name, sentences=5)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=5)
    except:
        return "No Wikipedia data found."

# Function to fetch recent news headlines
def fetch_news(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&sortBy=relevancy&apiKey={NEWS_API_KEY}&pageSize=5"
    response = requests.get(url)
    data = response.json()
    headlines = [article['title'] for article in data.get('articles', [])]
    return headlines if headlines else ["No news found"]

# Streamlit UI
st.title("HR Due Diligence Tool")

company_name = st.text_input("Enter company name:")

if company_name:
    st.subheader("Wikipedia Overview")
    wiki_summary = fetch_wiki_summary(company_name)
    st.write(wiki_summary)

    st.subheader("Recent News Headlines")
    news_headlines = fetch_news(company_name)
    for idx, headline in enumerate(news_headlines, 1):
        st.write(f"{idx}. {headline}")

    # Combine text for word cloud & sentiment
    combined_text = wiki_summary + " " + " ".join(news_headlines)

    # WordCloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(combined_text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    # Optional: download report
    from io import BytesIO
    report_text = f"Company: {company_name}\n\nWikipedia Summary:\n{wiki_summary}\n\nNews Headlines:\n" + "\n".join(news_headlines)
    st.download_button("Download Report", report_text, file_name=f"{company_name}_report.txt")

import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re

# ====== CONFIG ======
API_KEY = os.getenv("NEWSDATA_API_KEY")
if not API_KEY:
    st.error("API key not set! Please add it in CloudStream Secrets.")
    st.stop()

NEWS_BASE_URL = "https://newsdata.io/api/1/news"
GOOGLE_SEARCH_URL = "https://www.google.com/search?q="

# ====== HELPER FUNCTIONS ======
def fetch_news(company_name, max_results=5):
    """Fetch news articles about the company from NewsData.io"""
    params = {"apikey": API_KEY, "q": company_name, "language": "en", "page": 1}
    try:
        response = requests.get(NEWS_BASE_URL, params=params, timeout=10)
        data = response.json()
        if data.get("status") != "success":
            return {"error": "API returned non-success status", "data": data}
        articles = data.get("results", [])[:max_results]
        if not articles:
            return {"message": f"No news found for '{company_name}'"}
        return [
            {"title": a.get("title"), "link": a.get("link"),
             "pubDate": a.get("pubDate"), "source": a.get("source_id")}
            for a in articles
        ]
    except Exception as e:
        return {"error": str(e)}

def fetch_google_snippets(company_name, max_results=5):
    """Scrape top Google search snippets for the company"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(GOOGLE_SEARCH_URL + company_name, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        snippets = []
        for g in soup.find_all('div', class_='tF2Cxc')[:max_results]:
            title_tag = g.find('h3')
            link_tag = g.find('a')
            snippet_tag = g.find('span', class_='aCOpRe')
            if title_tag and link_tag and snippet_tag:
                snippets.append({
                    "title": title_tag.get_text(),
                    "link": link_tag['href'],
                    "snippet": snippet_tag.get_text()
                })
        if not snippets:
            return {"message": f"No Google snippets found for '{company_name}'"}
        return snippets
    except Exception as e:
        return {"error": str(e)}

def fetch_company_reputation(company_name):
    """Basic reputation check via Google search keywords"""
    keywords = ["reviews", "employee satisfaction", "ratings", "Glassdoor"]
    reputation_info = {}
    for kw in keywords:
        snippets = fetch_google_snippets(f"{company_name} {kw}", max_results=3)
        reputation_info[kw] = snippets
    return reputation_info

def extract_text_for_wordcloud(news, snippets):
    """Combine news titles and Google snippets to generate text for word cloud"""
    text_parts = []
    if isinstance(news, list):
        text_parts.extend([a["title"] for a in news if "title" in a])
    if isinstance(snippets, list):
        text_parts.extend([s["snippet"] for s in snippets if "snippet" in s])
    combined_text = " ".join(text_parts)
    # Clean text
    combined_text = re.sub(r'[^A-Za-z\s]', '', combined_text)
    return combined_text

def generate_wordcloud(text):
    """Generate a WordCloud object from text"""
    if not text.strip():
        return None
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    return wordcloud

# ====== STREAMLIT UI ======
st.set_page_config(page_title="HR Due Diligence Tool", layout="wide")
st.title("HR Due Diligence Dashboard")
st.markdown(
    "Enter the company name to fetch news, Google snippets, reputation info, and a word cloud for culture analysis."
)

company_input = st.text_input("Company Name", "")

if st.button("Fetch Data") and company_input.strip():
    with st.spinner(f"Fetching data for {company_input}..."):
        news = fetch_news(company_input.strip())
        google_snippets = fetch_google_snippets(company_input.strip())
        reputation = fetch_company_reputation(company_input.strip())
        
        # Generate word cloud
        text_for_wc = extract_text_for_wordcloud(news if isinstance(news, list) else [], 
                                                 google_snippets if isinstance(google_snippets, list) else [])
        wordcloud = generate_wordcloud(text_for_wc)
    
    # JSON output
    st.subheader("Raw JSON Data")
    st.json({
        "company": company_input.strip(),
        "news": news,
        "google_snippets": google_snippets,
        "reputation": reputation
    })
    
    # Word Cloud output
    st.subheader("Culture / Sentiment Word Cloud")
    if wordcloud:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("No text available for word cloud.")
        
elif company_input.strip() == "":
    st.info("Please enter a company name to fetch data.")

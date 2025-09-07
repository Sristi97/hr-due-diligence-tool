# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
import re
import json
import time

st.set_page_config(page_title="HR Due Diligence Tool", layout="wide")
st.title("🕵️ HR Due Diligence — HR Due Diligence Tool (Prototype)")
st.markdown("Enter a company name and the tool will pull public snippets and news, perform sentiment & theme analysis, and produce a quick HR DD summary.")

# -------------------------
# Helpers
# -------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0 Safari/537.36"
}

@st.cache_data(show_spinner=False)
def fetch_news_newsdata(company: str, api_key: str, page_size: int = 8):
    """Fetch news articles using NewsData.io (returns list of (title, description, link, source, pubDate))."""
    if not api_key:
        return []
    url = "https://newsdata.io/api/1/news"
    params = {"apikey": api_key, "q": company, "language": "en", "page": 1}
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return []
        data = resp.json()
        results = data.get("results", [])[:page_size]
        out = []
        for a in results:
            title = a.get("title", "") or ""
            desc = a.get("description", "") or ""
            link = a.get("link", "") or a.get("source", "")
            source = a.get("source_id", "") or ""
            pubDate = a.get("pubDate", "") or ""
            out.append({"title": title, "description": desc, "link": link, "source": source, "pubDate": pubDate})
        return out
    except Exception:
        return []

@st.cache_data(show_spinner=False)
def fetch_google_snippets(company: str, num_results: int = 8, pause: float = 1.0):
    """
    Lightweight Google search snippet fetcher: fetches search result snippets for queries like:
    "COMPANY employee reviews site:glassdoor.com" and a generic culture query.
    NOTE: This is an unofficial scraper. Keep usage light or switch to a SERP API for production.
    """
    snippets = []
    queries = [
        f'{company} employee reviews site:glassdoor.com',
        f'{company} company reviews',
        f'{company} work culture',
        f'{company} employees complain'
    ]
    for q in queries:
        # Respectful pause
        time.sleep(pause)
        q_enc = requests.utils.quote(q)
        url = f"https://www.google.com/search?q={q_enc}&num={num_results}"
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            # Try multiple selectors to be robust
            # Common Google snippet containers: 'div.VwiC3b', 'div.IsZvec', 'div.BNeawe.s3v9rd'
            selectors = [
                ('div', {'class': 'VwiC3b'}),
                ('div', {'class': 'IsZvec'}),
                ('div', {'class': 'BNeawe s3v9rd'}),
            ]
            found = False
            for tag, attrs in selectors:
                hits = soup.find_all(tag, attrs=attrs)
                if hits:
                    for h in hits:
                        text = h.get_text(separator=" ", strip=True)
                        if text:
                            snippets.append(text)
                    found = True
            # Fallback: search for <span> in result blocks
            if not found:
                for g in soup.find_all('div', class_='g'):
                    txt = g.get_text(separator=" ", strip=True)
                    if txt:
                        snippets.append(txt)
        except Exception:
            # ignore individual query failures
            continue
    # dedupe & limit
    unique = []
    for s in snippets:
        if s not in unique:
            unique.append(s)
    return unique[:num_results]

def sentiment_label_from_score(score: float, pos=0.1, neg=-0.1):
    if score > pos: return "Positive"
    if score < neg: return "Negative"
    return "Neutral"

def extract_keywords(text: str, top_n=8):
    # simple tokenization + stopword removal using wordcloud STOPWORDS
    words = re.findall(r"[A-Za-z']{3,}", text.lower())
    stop = set(STOPWORDS)
    filtered = [w for w in words if w not in stop]
    counts = Counter(filtered)
    return [w for w, _ in counts.most_common(top_n)]

def load_sample_reviews_for_company(company: str):
    # optional fallback if google snippets are empty; file should be present in repo
    try:
        with open("sample_reviews.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(company.lower(), [])
    except Exception:
        return []

# -------------------------
# UI inputs
# -------------------------
with st.sidebar:
    st.markdown("**Inputs**")
    company = st.text_input("Company name", value="Reliance Industries")
    news_api_key = st.text_input("NewsData.io API Key (paste here)", type="password")
    run = st.button("Run HR DD Analysis")

# -------------------------
# Main run
# -------------------------
if run:
    if not company or company.strip() == "":
        st.error("Please enter a company name.")
    else:
        company = company.strip()
        # Summary card placeholders
        culture_verdict = "Unknown"
        reputation_verdict = "Unknown"
        culture_score = 0.0
        reputation_score = 0.0
        combined_keywords = []

        with st.spinner("Fetching culture snippets from Google..."):
            snippets = fetch_google_snippets(company, num_results=8)
        if not snippets:
            # fallback to sample reviews file (if present)
            sample = load_sample_reviews_for_company(company)
            if sample:
                # sample is expected list of dicts with 'review' key OR list of strings
                fallback_texts = []
                for entry in sample:
                    if isinstance(entry, dict):
                        fallback_texts.append(entry.get("review", ""))
                    else:
                        fallback_texts.append(str(entry))
                snippets = fallback_texts
        # analyze culture snippets
        if snippets:
            culture_text = " ".join(snippets)
            culture_scores = [TextBlob(s).sentiment.polarity for s in snippets if s.strip()]
            culture_score = sum(culture_scores)/len(culture_scores) if culture_scores else 0.0
            culture_verdict = sentiment_label_from_score(culture_score)
            culture_keywords = extract_keywords(culture_text, top_n=6)
        else:
            culture_text = ""
            culture_keywords = []

        # News / reputation
        with st.spinner("Fetching news (NewsData.io)..."):
            news_articles = fetch_news_newsdata(company, news_api_key, page_size=8)
        if news_articles:
            news_texts = [ (a["title"] + " " + (a["description"] or "")) for a in news_articles ]
            reputation_scores = [TextBlob(t).sentiment.polarity for t in news_texts if t.strip()]
            reputation_score = sum(reputation_scores)/len(reputation_scores) if reputation_scores else 0.0
            reputation_verdict = sentiment_label_from_score(reputation_score)
            news_keywords = extract_keywords(" ".join(news_texts), top_n=6)
        else:
            news_texts = []
            news_keywords = []

        # combined keywords
        combined_keywords = (culture_keywords + news_keywords)
        # dedupe keep order
        seen = set()
        combined_keywords = [k for k in combined_keywords if not (k in seen or seen.add(k))][:8]

        # -------------------------
        # Summary card
        # -------------------------
        st.markdown("## Quick HR DD Summary")
        col_a, col_b, col_c = st.columns([1,1,1])
        col_a.metric("Culture (snippets)", culture_verdict, f"{culture_score:.2f}")
        col_b.metric("Reputation (news)", reputation_verdict, f"{reputation_score:.2f}")
        col_c.write("**Key Themes**")
        if combined_keywords:
            col_c.write(", ".join(combined_keywords))
        else:
            col_c.write("—")

        st.markdown("---")

        # -------------------------
        # Detailed tiles (3 columns)
        # -------------------------
        c1, c2 = st.columns([1.2, 1])
        # Left: Culture details
        with c1:
            st.header("💬 Culture & Employee Snippets")
            if snippets:
                for i, s in enumerate(snippets[:6], 1):
                    st.info(f"{i}. {s}")
                st.subheader("Culture sentiment")
                st.write(f"Verdict: **{culture_verdict}** (avg polarity {culture_score:.2f})")
                if culture_keywords:
                    st.write("Themes:", ", ".join(culture_keywords))
            else:
                st.warning("No culture snippets found. Consider adding a sample_reviews.json fallback or using SERP API.")

            # small download of culture findings
            culture_report = f"Company: {company}\n\nCulture Verdict: {culture_verdict} ({culture_score:.2f})\n\nTop themes: {', '.join(culture_keywords)}\n\nSnippets:\n" + "\n".join(snippets)
            st.download_button("Download culture report (.txt)", culture_report, file_name=f"{company}_culture.txt")

        # Right: News and WordCloud
        with c2:
            st.header("📰 Reputation (News)")

            if news_articles:
                for i, a in enumerate(news_articles[:6], 1):
                    title = a.get("title") or ""
                    desc = a.get("description") or ""
                    src = a.get("source") or ""
                    pub = a.get("pubDate") or ""
                    link = a.get("link") or ""
                    # sentiment per article
                    sscore = TextBlob((title + " " + desc)).sentiment.polarity
                    slabel = sentiment_label_from_score(sscore)
                    if slabel == "Positive":
                        badge = ":green_circle:"
                    elif slabel == "Negative":
                        badge = ":red_circle:"
                    else:
                        badge = ":white_circle:"
                    st.markdown(f"**{i}. [{title}]({link})**  \n{desc}  \nSource: {src} • {pub}  \nSentiment: {slabel} ({sscore:.2f}) {badge}")
                    st.markdown("---")
                st.subheader("Reputation word cloud")
                wc_text = " ".join(news_texts)
                if wc_text.strip():
                    wc = WordCloud(width=600, height=300, background_color="white", stopwords=STOPWORDS, max_words=35).generate(wc_text)
                    fig, ax = plt.subplots(figsize=(6,3))
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)
                else:
                    st.write("No text for word cloud.")
                # downloadable combined report
                combined_report = f"Company: {company}\n\nCulture: {culture_verdict} ({culture_score:.2f})\nReputation: {reputation_verdict} ({reputation_score:.2f})\n\nKey themes: {', '.join(combined_keywords)}\n\nTop news:\n"
                for a in news_articles[:10]:
                    combined_report += f"- {a.get('title','')} — {a.get('link','')}\n"
                st.download_button("Download consolidated report (.txt)", combined_report, file_name=f"{company}_hrdd_report.txt")
            else:
                st.warning("No news articles found or invalid NewsData.io key. Enter a valid key in the sidebar.")

import json
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download NLTK data if not already
nltk.download('vader_lexicon')

st.set_page_config(page_title="HR Due Diligence Tool", layout="wide")
st.title("HR Due Diligence Tool – Prototype")

# Load sample reviews
with open("sample_reviews.json") as f:
    data = json.load(f)

# Input company name
company = st.text_input("Enter Company Name (e.g., TCS, Infosys, Wipro)")

if company:
    reviews = data.get(company)
    if not reviews:
        st.warning("No data available for this company.")
    else:
        st.subheader("Reviews")
        for i, review in enumerate(reviews, 1):
            st.write(f"{i}. {review}")

        # Sentiment Analysis
        sid = SentimentIntensityAnalyzer()
        scores = [sid.polarity_scores(r)['compound'] for r in reviews]
        avg_score = sum(scores)/len(scores)

        if avg_score >= 0.05:
            verdict = "Overall Positive"
        elif avg_score <= -0.05:
            verdict = "Overall Negative"
        else:
            verdict = "Neutral / Mixed"

        st.subheader("Sentiment Analysis")
        st.write(f"Average Sentiment Score: {avg_score:.2f}")
        st.write(f"Verdict: {verdict}")

        # Word Cloud
        st.subheader("Key Themes (Word Cloud)")
        text = " ".join(reviews)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Top Keywords
        st.subheader("Top Keywords")
        words = text.split()
        freq = {}
        for w in words:
            w = w.lower().strip(".,")
            freq[w] = freq.get(w,0)+1
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
        for word, count in sorted_words:
            st.write(f"{word}: {count}")

        # Downloadable report
        st.subheader("Download Report")
        report_text = f"Company: {company}\n\nReviews:\n"
        report_text += "\n".join([f"{i}. {r}" for i,r in enumerate(reviews,1)])
        report_text += f"\n\nSentiment Score: {avg_score:.2f}\nVerdict: {verdict}\n\nTop Keywords:\n"
        report_text += "\n".join([f"{w}: {c}" for w,c in sorted_words])

        st.download_button("Download TXT Report", report_text, file_name=f"{company}_HR_Report.txt")

import streamlit as st
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- Load sample JSON data ---
with open("sample_reviews.json") as f:
    data = json.load(f)

# --- Page Configuration ---
st.set_page_config(
    page_title="HR Due Diligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Title ---
st.title("HR Due Diligence Dashboard")

# --- Company Input ---
company_input = st.text_input("Enter Company Name:", value="Reliance").strip()

if company_input in data:
    company_data = data[company_input]
    
    # --- Reputation Section ---
    st.subheader("Reputation & Ratings")
    rep = company_data["reputation"]
    st.metric("Total Reviews", rep["reviews"])
    st.metric("Employee Satisfaction", rep["employee_satisfaction"])
    st.metric("Overall Ratings", rep["ratings"])
    st.metric("Glassdoor Rating", rep["Glassdoor"])
    
    # --- Culture / Sentiment Word Cloud ---
    st.subheader("Culture / Sentiment Word Cloud")
    words = company_data.get("culture_sentiment", [])
    if words:
        text = " ".join(words)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10,5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.info("No text available for word cloud.")
else:
    st.warning(f"No data available for '{company_input}'. Showing placeholder data.")
    
    # --- Placeholder Data ---
    st.subheader("Reputation & Ratings")
    st.metric("Total Reviews", "N/A")
    st.metric("Employee Satisfaction", "N/A")
    st.metric("Overall Ratings", "N/A")
    st.metric("Glassdoor Rating", "N/A")
    
    st.subheader("Culture / Sentiment Word Cloud")
    st.info("No text available for word cloud.")

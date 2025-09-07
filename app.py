import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ------------------------
# Sample Data
# ------------------------
company_data = {
    "Reliance": {
        "reputation": {
            "reviews": "4.1/5",
            "employee_satisfaction": "Good",
            "ratings": "4/5"
        },
        "culture": "Innovative, Collaborative, Fast-paced, Customer-focused",
    },
    "Tata": {
        "reputation": {
            "reviews": "3.9/5",
            "employee_satisfaction": "Moderate",
            "ratings": "3.8/5"
        },
        "culture": "Ethical, Team-oriented, Sustainable, Respectful",
    }
}

# ------------------------
# Dummy data generator
# ------------------------
def generate_dummy_data(company_name):
    dummy_reviews = ["4.0/5", "Good", "3.8/5", "3.5/5", "Excellent", "Average"]
    dummy_culture_words = [
        "Innovative", "Collaborative", "Supportive", "Fast-paced",
        "Flexible", "Inclusive", "Customer-focused", "Ethical"
    ]
    return {
        "reputation": {
            "reviews": random.choice(dummy_reviews),
            "employee_satisfaction": random.choice(dummy_reviews),
            "ratings": random.choice(dummy_reviews)
        },
        "culture": ", ".join(random.sample(dummy_culture_words, 4))
    }

# ------------------------
# Streamlit Config
# ------------------------
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")

# ------------------------
# Sidebar for Company Input
# ------------------------
st.sidebar.title("HR Due Diligence Tool")
company_name = st.sidebar.text_input("Enter Company Name:", "").strip()

st.title("HR Due Diligence Dashboard")

if company_name:
    company_info = company_data.get(company_name, generate_dummy_data(company_name))

    # ------------------------
    # Top Metrics
    # ------------------------
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Reviews", company_info["reputation"]["reviews"])
    col2.metric("Employee Satisfaction", company_info["reputation"]["employee_satisfaction"])
    col3.metric("Ratings", company_info["reputation"]["ratings"])

    # ------------------------
    # Culture & Sentiment Word Cloud (small)
    # ------------------------
    st.subheader("Culture & Sentiment")
    col_wc, col_dummy = st.columns([2, 1])  # smaller wordcloud, empty column for spacing
    culture_text = company_info.get("culture", "")
    if culture_text:
        wordcloud = WordCloud(width=400, height=200, background_color="white").generate(culture_text)
        plt.figure(figsize=(6, 3))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        col_wc.pyplot(plt)
    else:
        col_wc.write("No culture text available.")

    # ------------------------
    # Highlights & Sample Feedback side by side
    # ------------------------
    st.subheader("HR Insights")
    col_high, col_feedback = st.columns(2)

    # Key Highlights
    highlights = [
        f"{company_name} has a collaborative and supportive culture.",
        f"{company_name} focuses on innovation and employee growth.",
        f"{company_name} maintains fair performance evaluations.",
        f"{company_name} encourages learning and development."
    ]
    col_high.markdown("**Key Highlights**")
    for h in random.sample(highlights, k=3):
        col_high.success(h)

    # Sample Feedback in expanders
    sample_feedbacks = [
        f"{company_name} provides great career growth opportunities.",
        f"{company_name} has a supportive management team.",
        f"Work-life balance at {company_name} is good.",
        f"{company_name} encourages learning and innovation.",
        f"{company_name} values diversity and inclusion.",
        f"{company_name} rewards high performance appropriately."
    ]
    col_feedback.markdown("**Sample Employee Feedback**")
    for fb in random.sample(sample_feedbacks, k=3):
        with col_feedback.expander("View Feedback"):
            st.info(fb)

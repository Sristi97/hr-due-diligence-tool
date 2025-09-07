import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ------------------------
# Sample Data (dummy JSON)
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
# Function to generate dummy data if company not in JSON
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
# Streamlit App
# ------------------------
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

# Initialize session state
if "company_name" not in st.session_state:
    st.session_state.company_name = ""

# Input for company name
company_name = st.text_input("Enter Company Name:", value=st.session_state.company_name).strip()
st.session_state.company_name = company_name

if company_name:
    company_info = company_data.get(company_name, generate_dummy_data(company_name))

    # ------------------------
    # Dashboard metrics
    # ------------------------
    st.subheader(f"Company: {company_name}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Reviews", company_info["reputation"]["reviews"])
    col2.metric("Employee Satisfaction", company_info["reputation"]["employee_satisfaction"])
    col3.metric("Ratings", company_info["reputation"]["ratings"])

    # ------------------------
    # Culture & Sentiment Word Cloud
    # ------------------------
    st.subheader("Culture & Sentiment Word Cloud")
    culture_text = company_info.get("culture", "")
    if culture_text:
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(culture_text)
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.write("No culture text available.")

    # ------------------------
    # Sample Employee Feedback
    # ------------------------
    st.subheader("Sample Employee Feedback")
    sample_feedbacks = [
        f"{company_name} provides great career growth opportunities.",
        f"{company_name} has a supportive management team.",
        f"Work-life balance at {company_name} is good.",
        f"{company_name} encourages learning and innovation.",
        f"{company_name} values diversity and inclusion.",
        f"{company_name} rewards high performance appropriately."
    ]
    for fb in random.sample(sample_feedbacks, k=3):
        st.info(fb)

import streamlit as st
import json
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")

# Title
st.title("HR Due Diligence Dashboard")
st.write("Analyze company reputation, culture, and employee sentiment at a glance.")

# Load sample JSON data
try:
    with open("sample_reviews.json") as f:
        company_data = json.load(f)
except Exception as e:
    st.error("Failed to load sample_reviews.json")
    company_data = {}

# --- Function to generate dummy data ---
def generate_dummy_data(company_name):
    dummy_reviews = random.randint(50, 500)
    dummy_satisfaction = round(random.uniform(3.0, 4.5), 2)
    dummy_rating = round(random.uniform(3.0, 4.5), 2)
    dummy_culture_texts = [
        f"{company_name} values innovation, teamwork, and integrity.",
        f"{company_name} fosters collaboration and employee growth.",
        f"{company_name} encourages transparency, diversity, and accountability.",
        f"{company_name} has a supportive and inclusive workplace culture."
    ]
    dummy_culture = random.choice(dummy_culture_texts)
    
    return {
        "reputation": {
            "reviews": dummy_reviews,
            "employee_satisfaction": dummy_satisfaction,
            "ratings": dummy_rating
        },
        "culture": dummy_culture
    }

# --- Company input ---
company_name = st.text_input("Enter Company Name:", "Reliance").strip()

# --- Fetch data or fallback to dummy ---
company_info = company_data.get(company_name, generate_dummy_data(company_name))

# --- Show HR Metrics ---
st.subheader(f"Company: {company_name}")
col1, col2, col3 = st.columns(3)

col1.metric("Reviews", company_info["reputation"]["reviews"])
col2.metric("Employee Satisfaction", company_info["reputation"]["employee_satisfaction"])
col3.metric("Ratings", company_info["reputation"]["ratings"])

# --- Culture / Sentiment Word Cloud ---
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

# --- Optional: Employee Reviews Section ---
st.subheader("Sample Employee Feedback")
sample_feedbacks = [
    f"{company_name} provides great career growth opportunities.",
    f"{company_name} has a supportive management team.",
    f"Work-life balance at {company_name} is good.",
    f"{company_name} encourages learning and innovation."
]
for fb in random.sample(sample_feedbacks, k=2):
    st.info(fb)

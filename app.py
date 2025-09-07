import streamlit as st
import json
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")

# Load sample JSON data
with open("sample_reviews.json", "r") as f:
    sample_data = json.load(f)

# --- Functions ---

def generate_dummy_feedback():
    pool = [
        "good work-life balance", "supportive management", "decent benefits",
        "challenging work", "excellent team collaboration", "limited training programs",
        "fast-paced environment", "flexible work hours", "recognition is fair"
    ]
    return random.sample(pool, 5)

def generate_dummy_metrics():
    return {
        "reviews_count": random.randint(20, 200),
        "employee_satisfaction": random.randint(60, 95),
        "overall_rating": round(random.uniform(3.0, 4.8), 1)
    }

def generate_dummy_culture():
    keywords = ["Innovation", "Collaboration", "Diversity", "Integrity", 
                "Learning", "Transparency", "Inclusion", "Flexibility", "Accountability", "Teamwork"]
    random.shuffle(keywords)
    return keywords[:5]

def generate_summary(company_name, metrics, feedback_list, culture_words):
    return (
        f"{company_name} has {metrics['reviews_count']} employee reviews, "
        f"with an overall satisfaction of {metrics['employee_satisfaction']}% "
        f"and an average rating of {metrics['overall_rating']}. "
        f"The company culture emphasizes {', '.join(culture_words)}. "
        f"Employees mention {', '.join(feedback_list[:3])} among other things."
    )

# --- UI ---

st.title("HR Due Diligence Dashboard")
st.markdown("Enter a company name to generate HR insights:")

company_name = st.text_input("", "").strip()

if company_name:
    key = company_name.lower()
    if key in sample_data:
        info = sample_data[key]
        feedback_list = info.get("employee_feedback", [])
        metrics = info.get("metrics", {})
        culture_words = info.get("culture_words", [])
    else:
        feedback_list = generate_dummy_feedback()
        metrics = generate_dummy_metrics()
        culture_words = generate_dummy_culture()

    # --- Summary ---
    st.subheader("Executive Summary")
    st.markdown(generate_summary(company_name, metrics, feedback_list, culture_words))

    # --- Metrics ---
    st.subheader("Key HR Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Reviews", metrics.get("reviews_count", 0))
    col2.metric("Employee Satisfaction (%)", metrics.get("employee_satisfaction", 0))
    col3.metric("Overall Rating", metrics.get("overall_rating", 0))

    # --- Employee Feedback ---
    st.subheader("Employee Feedback")
    for feedback in feedback_list:
        with st.expander(feedback[:50] + "..."):
            st.write(feedback)

    # --- Culture Word Cloud ---
    st.subheader("Culture & Sentiment Word Cloud")
    culture_text = " ".join(culture_words)
    if culture_text:
        wc = WordCloud(width=800, height=300, background_color="white", colormap="Set2").generate(culture_text)
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.write("No culture keywords available.")

else:
    st.info("Please enter a company name above to view HR insights.")

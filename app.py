import streamlit as st
import json
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")

# Load sample JSON data
with open("sample_reviews.json", "r") as f:
    sample_data = json.load(f)

# Dummy data generators
def generate_dummy_feedback():
    pool = [
        "Good work-life balance but growth could improve.",
        "Supportive management and decent benefits.",
        "Challenging work but excellent team collaboration.",
        "Training is limited but peers are helpful.",
        "Fast-paced environment with good learning opportunities.",
        "Management listens but execution is slow.",
        "Flexible hours and positive culture.",
        "High workload but recognition is fair."
    ]
    return random.sample(pool, k=5)

def generate_dummy_metrics():
    return {
        "reviews_count": random.randint(20, 200),
        "employee_satisfaction": random.randint(60, 95),
        "overall_rating": round(random.uniform(3.0, 4.8), 1)
    }

def generate_dummy_culture():
    keywords = ["Innovation", "Collaboration", "Diversity", "Integrity",
                "Learning", "Transparency", "Inclusion", "Flexibility", "Accountability"]
    random.shuffle(keywords)
    return keywords[:7]

# Generate human-readable summary
def generate_summary(company_name, metrics, feedback_list, culture_words):
    review_count = metrics.get("reviews_count", 50)
    satisfaction = metrics.get("employee_satisfaction", 75)
    rating = metrics.get("overall_rating", 4.0)
    
    culture_summary = ", ".join(culture_words) if culture_words else "various aspects of culture"
    feedback_summary = ", ".join([f.split(",")[0] for f in feedback_list[:3]]) + "."

    summary = (
        f"**HR Due Diligence Summary for {company_name}**\n\n"
        f"Based on an analysis of {review_count} employee reviews, the overall employee satisfaction is approximately "
        f"{satisfaction}%, with an average rating of {rating}. Employees emphasize {culture_summary}. "
        f"Feedback highlights {feedback_summary}"
    )
    return summary

# --- UI START ---
st.title("HR Due Diligence Dashboard")
st.markdown("Enter a company name to generate HR insights:")

company_name = st.text_input("Company Name", "").strip()

if company_name:
    company_key = company_name.lower()
    
    if company_key in sample_data:
        company_info = sample_data[company_key]
        feedback_list = company_info.get("employee_feedback", [])
        metrics = company_info.get("metrics", {})
        culture_words = company_info.get("culture_words", [])
    else:
        # Use dummy data
        feedback_list = generate_dummy_feedback()
        metrics = generate_dummy_metrics()
        culture_words = generate_dummy_culture()
    
    # --- Summary ---
    st.subheader("Summary")
    st.markdown(generate_summary(company_name, metrics,

import streamlit as st
import json
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")

# Load sample JSON data
with open("sample_reviews.json", "r") as f:
    sample_data = json.load(f)

# Function to generate random dummy feedback if company not in JSON
def generate_dummy_feedback():
    feedback_pool = [
        "Good work-life balance, but growth opportunities could improve.",
        "Supportive management, decent benefits.",
        "Challenging work, team collaboration is excellent.",
        "Training programs are limited, but peers are helpful.",
        "Fast-paced environment, learning opportunities are good.",
        "Management listens but execution can be slow.",
        "Flexible work hours and positive team culture.",
        "Workload can be high, but recognition is fair.",
    ]
    return random.sample(feedback_pool, k=5)

# Function to generate dummy ratings and satisfaction
def generate_dummy_metrics():
    return {
        "reviews_count": random.randint(20, 200),
        "employee_satisfaction": random.randint(60, 95),
        "overall_rating": round(random.uniform(3.0, 4.8), 1)
    }

# Function to generate dummy culture keywords
def generate_dummy_culture():
    keywords = ["Innovation", "Collaboration", "Diversity", "Integrity", 
                "Learning", "Transparency", "Inclusion", "Flexibility", "Accountability"]
    random.shuffle(keywords)
    return keywords[:7]

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
        # Use dynamic dummy data
        feedback_list = generate_dummy_feedback()
        metrics = generate_dummy_metrics()
        culture_words = generate_dummy_culture()
    
    # Summary Metrics
    st.subheader(f"HR Metrics for {company_name}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Reviews", metrics.get("reviews_count", 0))
    col2.metric("Employee Satisfaction (%)", metrics.get("employee_satisfaction", 0))
    col3.metric("Overall Rating", metrics.get("overall_rating", 0))

    # Employee Feedback
    st.subheader("Employee Feedback")
    for feedback in feedback_list:
        st.write(f"- {feedback}")

    # Culture / Sentiment Word Cloud
    st.subheader("Culture / Sentiment Word Cloud")
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

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
# Company Input
# ------------------------
st.title("HR Due Diligence Dashboard")
company_name = st.text_input("Enter Company Name:", "").strip()

if company_name:
    company_info = company_data.get(company_name, generate_dummy_data(company_name))

    # ------------------------
    # Summary Section
    # ------------------------
    st.subheader("Summary")
    summary_text = (
        f"{company_name} has a workforce culture that emphasizes collaboration and innovation. "
        f"Overall employee satisfaction is {company_info['reputation']['employee_satisfaction']} "
        f"with average ratings of {company_info['reputation']['ratings']}. "
        f"Key cultural attributes include {company_info.get('culture', 'N/A')}."
    )
    st.info(summary_text)

    # ------------------------
    # Top Metrics
    # ------------------------
    st.subheader("Key Metrics")
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
        wordcloud = WordCloud(width=400, height=200, background_color="white").generate(culture_text)
        plt.figure(figsize=(6, 3))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.write("No culture text available.")

    # ------------------------
    # Employee Feedback in two columns
    # ------------------------
    st.subheader("Employee Feedback")
    col_feedback1, col_feedback2 = st.columns(2)

    feedback_list = [
        f"{company_name} provides great career growth opportunities.",
        f"{company_name} has a supportive management team.",
        f"Work-life balance at {company_name} is good.",
        f"{company_name} encourages learning and innovation.",
        f"{company_name} values diversity and inclusion.",
        f"{company_name} rewards high performance appropriately."
    ]

    feedback_sample = random.sample(feedback_list, k=4)
    for i, fb in enumerate(feedback_sample):
        if i % 2 == 0:
            col_feedback1.write(f"- {fb}")
        else:
            col_feedback2.write(f"- {fb}")

# app.py
import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---------------------------
# Dummy Data Generators
# ---------------------------

def generate_summary(company):
    strengths = ["supportive management", "flexible work hours", "innovative culture", "strong training programs", "team collaboration"]
    weaknesses = ["slow decision-making", "limited recognition", "high workload", "training gaps", "internal politics"]
    summary = (
        f"{company} has strengths in {random.choice(strengths)} and {random.choice(strengths)}. "
        f"Areas of improvement include {random.choice(weaknesses)} and {random.choice(weaknesses)}. "
        f"Overall, the employee sentiment is {'positive' if random.random() > 0.3 else 'mixed'}."
    )
    return summary

def generate_metrics():
    return {
        "Employee Count": random.randint(200, 5000),
        "Attrition %": round(random.uniform(5, 25), 1),
        "Average Tenure (yrs)": round(random.uniform(1, 10), 1),
        "Satisfaction %": random.randint(60, 95),
        "Overall Rating": round(random.uniform(2.5, 5.0), 1)
    }

def generate_feedback():
    positive_feedback = [
        "Supportive team culture",
        "Opportunities to learn",
        "Good work-life balance",
        "Flexible hours",
        "Strong leadership"
    ]
    negative_feedback = [
        "High workload pressure",
        "Limited recognition",
        "Slow decision-making",
        "Training gaps",
        "Internal politics"
    ]
    # Random selection
    pos = random.sample(positive_feedback, k=3)
    neg = random.sample(negative_feedback, k=3)
    return pos, neg

def generate_culture_keywords():
    keywords = ["Innovation", "Collaboration", "Integrity", "Learning", "Accountability", "Diversity", "Empathy", "Agility"]
    word_freq = {k: random.randint(5,20) for k in random.sample(keywords, k=len(keywords))}
    return word_freq

def generate_highlights():
    highlights = [
        "Employees appreciate collaborative work environment.",
        "Training programs are improving but still limited in reach.",
        "Management is supportive but decision-making can be slow.",
        "Work-life balance is rated highly among teams.",
        "Recognition programs are not consistent across departments."
    ]
    return random.sample(highlights, k=3)

# ---------------------------
# Streamlit Layout
# ---------------------------

st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")

st.title("HR Due Diligence Dashboard")

# Company Input
company = st.text_input("Enter Company Name", value="").strip()

if company:
    # Generate dummy data
    summary = generate_summary(company)
    metrics = generate_metrics()
    pos_feedback, neg_feedback = generate_feedback()
    culture_keywords = generate_culture_keywords()
    highlights = generate_highlights()
    
    # Summary
    st.subheader("Executive Summary")
    st.write(summary)
    
    # Metrics in 3 columns
    st.subheader("Key HR Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Employee Count", metrics["Employee Count"])
    col1.metric("Attrition %", f"{metrics['Attrition %']}%")
    
    col2.metric("Average Tenure", f"{metrics['Average Tenure (yrs)']} yrs")
    col2.metric("Satisfaction %", f"{metrics['Satisfaction %']}%")
    
    col3.metric("Overall Rating", metrics["Overall Rating"])
    
    # Employee Feedback
    st.subheader("Employee Feedback")
    fb_col1, fb_col2 = st.columns(2)
    fb_col1.markdown("**Positive Feedback**")
    for f in pos_feedback:
        fb_col1.markdown(f"- {f}")
    fb_col2.markdown("**Negative Feedback**")
    for f in neg_feedback:
        fb_col2.markdown(f"- {f}")
    
    # Highlights
    st.subheader("Key Insights / Highlights")
    for h in highlights:
        st.markdown(f"- {h}")
    
    # Culture / Word Cloud
    st.subheader("Culture & Sentiment")
    fig, ax = plt.subplots(figsize=(10,4))
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(culture_keywords)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
    
else:
    st.info("Please enter a company name to generate the HR report.")

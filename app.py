import streamlit as st
import random
import json
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------------------------
# Load JSON Data
# ---------------------------
DATA_FILE = "sample_reviews.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        COMPANY_DATA = json.load(f)
else:
    COMPANY_DATA = {}

# ---------------------------
# Dummy Generators
# ---------------------------
def generate_random_summary(company):
    strengths = ["supportive management", "flexible work hours", "innovative culture",
                 "strong training programs", "team collaboration", "diverse teams"]
    weaknesses = ["slow decision-making", "limited recognition", "high workload",
                  "training gaps", "internal politics", "inconsistent policies"]
    culture_aspects = ["team collaboration", "innovation-driven environment",
                       "continuous learning", "employee engagement programs"]

    summary = (
        f"{company} has several strengths including {random.choice(strengths)} "
        f"and {random.choice(strengths)}. The company culture emphasizes "
        f"{random.choice(culture_aspects)}. Areas for improvement include "
        f"{random.choice(weaknesses)} and {random.choice(weaknesses)}. "
        f"Employee sentiment appears {'generally positive' if random.random() > 0.3 else 'mixed'}, "
        f"with feedback highlighting both achievements and challenges. Overall, {company} "
        f"presents an environment where employees experience growth opportunities while facing some operational challenges."
    )
    return summary

def generate_random_metrics():
    return {
        "Average Tenure (years)": round(random.uniform(2, 8), 1),
        "Annual Attrition Rate (%)": round(random.uniform(5, 25), 1),
        "Engagement Score (/5)": round(random.uniform(3.0, 5.0), 1),
        "Glassdoor Rating (/5)": round(random.uniform(2.5, 5.0), 1),
        "Satisfaction %": random.randint(60, 95)
    }

def generate_random_feedback():
    positive_feedback = [
        "Supportive team culture", "Opportunities to learn", "Good work-life balance",
        "Flexible hours", "Strong leadership", "Mentorship programs", "Inclusive environment"
    ]
    negative_feedback = [
        "High workload pressure", "Limited recognition", "Slow decision-making",
        "Training gaps", "Internal politics", "Inconsistent policies", "Promotion delays"
    ]
    pos = random.sample(positive_feedback, k=4)
    neg = random.sample(negative_feedback, k=4)
    return pos, neg

def generate_random_highlights():
    highlights = [
        "Employees appreciate collaborative work environment.",
        "Training programs are improving but still limited in reach.",
        "Management is supportive but decision-making can be slow.",
        "Work-life balance is rated highly among teams.",
        "Recognition programs are not consistent across departments.",
        "Innovation is encouraged but execution is sometimes delayed.",
        "Team engagement initiatives are increasing employee satisfaction."
    ]
    return random.sample(highlights, k=3)

def generate_culture_keywords():
    keywords = ["Innovation", "Collaboration", "Integrity", "Learning", "Accountability",
                "Diversity", "Empathy", "Agility", "Trust", "Communication"]
    word_freq = {k: random.randint(5, 20) for k in random.sample(keywords, k=len(keywords))}
    return word_freq

def generate_insights(summary, metrics, pos_feedback, neg_feedback):
    return (
        f"Based on available reviews, the overall employee satisfaction is around {metrics['Satisfaction %']}%. "
        f"Positive sentiment is mainly driven by factors such as {pos_feedback[0].lower()} and {pos_feedback[1].lower()}. "
        f"However, challenges like {neg_feedback[0].lower()} continue to impact perception. "
        f"Attrition at {metrics['Annual Attrition Rate (%)']}% suggests retention should be monitored closely. "
        f"Overall, the culture appears {'healthy and growth-oriented' if metrics['Satisfaction %'] > 75 else 'mixed, requiring management focus'}."
    )

# ---------------------------
# PDF Generator
# ---------------------------
def create_pdf(company, summary, metrics, pos_feedback, neg_feedback, highlights, insights):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"HR Due Diligence Report: {company}", ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Executive Summary:\n{summary}")

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Key HR Metrics", ln=True)
    pdf.set_font("Arial", '', 12)
    for k, v in metrics.items():
        pdf.cell(0, 10, f"- {k}: {v}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Positive Feedback", ln=True)
    pdf.set_font("Arial", '', 12)
    for f in pos_feedback:
        pdf.cell(0, 10, f"- {f}", ln=True)

    pdf.ln(2)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Negative Feedback", ln=True)
    pdf.set_font("Arial", '', 12)
    for f in neg_feedback:
        pdf.cell(0, 10, f"- {f}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Highlights", ln=True)
    pdf.set_font("Arial", '', 12)
    for h in highlights:
        pdf.cell(0, 10, f"- {h}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Consultant Insights", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, insights)

    file_path = f"{company}_HR_Report.pdf"
    pdf.output(file_path)
    return file_path

# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

company = st.text_input("Enter Company Name", value="").strip()

if company:
    if company in COMPANY_DATA:
        data = COMPANY_DATA[company]
        summary = data["summary"]
        metrics = data["metrics"]
        pos_feedback = data["positive_feedback"]
        neg_feedback = data["negative_feedback"]
        highlights = data["highlights"]
    else:
        summary = generate_random_summary(company)
        metrics = generate_random_metrics()
        pos_feedback, neg_feedback = generate_random_feedback()
        highlights = generate_random_highlights()

    insights = generate_insights(summary, metrics, pos_feedback, neg_feedback)

    # Executive Summary
    st.subheader("Executive Summary")
    st.write(summary)

    # Key HR Metrics (Cards instead of table)
    st.subheader("Key HR Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Average Tenure (years)", metrics["Average Tenure (years)"])
        st.metric("Engagement Score (/5)", metrics["Engagement Score (/5)"])

    with col2:
        st.metric("Annual Attrition Rate (%)", metrics["Annual Attrition Rate (%)"])
        st.metric("Glassdoor Rating (/5)", metrics["Glassdoor Rating (/5)"])

    with col3:
        st.metric("Satisfaction %", f"{metrics['Satisfaction %']}%")

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

    # Consultant Insights
    st.subheader("Consultant Insights")
    st.write(insights)

    # Culture & Word Cloud
    st.subheader("Culture & Sentiment")
    culture_keywords = generate_culture_keywords()
    fig, ax = plt.subplots(figsize=(10, 4))
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(culture_keywords)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # PDF Download
    pdf_file = create_pdf(company, summary, metrics, pos_feedback, neg_feedback, highlights, insights)
    with open(pdf_file, "rb") as f:
        st.download_button("Download Report as PDF", f, file_name=pdf_file, mime="application/pdf")

else:
    st.info("Please enter a company name to generate the HR report.")

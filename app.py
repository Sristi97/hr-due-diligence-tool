import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random
import json
from fpdf import FPDF

# ---------------------------
# Load Company Data
# ---------------------------
try:
    with open("sample_reviews.json", "r") as f:
        company_data = json.load(f)
except FileNotFoundError:
    company_data = {}

# ---------------------------
# Random Data Generators (fallback)
# ---------------------------
def generate_summary(company):
    strengths = ["supportive management", "flexible work hours", "innovative culture", "strong training programs"]
    weaknesses = ["slow decision-making", "limited recognition", "high workload", "internal politics"]
    culture_aspects = ["team collaboration", "innovation-driven environment", "continuous learning"]

    return (
        f"{company} has strengths like {random.choice(strengths)} and {random.choice(strengths)}. "
        f"The company culture emphasizes {random.choice(culture_aspects)}. "
        f"Areas for improvement include {random.choice(weaknesses)} and {random.choice(weaknesses)}. "
        f"Employee sentiment appears {'generally positive' if random.random() > 0.3 else 'mixed'}. "
        f"Overall, {company} presents growth opportunities with some operational challenges."
    )

def generate_metrics():
    return {
        "Number of Reviews": random.randint(50, 500),
        "Attrition %": round(random.uniform(5, 25), 1),
        "Average Tenure (yrs)": round(random.uniform(1, 10), 1),
        "Satisfaction %": random.randint(60, 95),
        "Overall Rating": round(random.uniform(2.5, 5.0), 1),
    }

def generate_feedback():
    positives = ["Supportive team culture", "Opportunities to learn", "Good work-life balance", "Strong leadership"]
    negatives = ["High workload", "Limited recognition", "Training gaps", "Internal politics"]
    return random.sample(positives, 3), random.sample(negatives, 3)

def generate_highlights():
    highlights = [
        "Employees appreciate collaborative work environment.",
        "Training programs improving but still limited in reach.",
        "Work-life balance is rated highly among teams.",
        "Recognition programs inconsistent across departments."
    ]
    return random.sample(highlights, 3)

def generate_culture_keywords():
    keywords = ["Innovation", "Collaboration", "Integrity", "Learning", "Diversity", "Trust"]
    return {k: random.randint(5, 20) for k in keywords}

def generate_insights(summary, metrics, pos_feedback, neg_feedback):
    return (
        f"Based on available reviews, the overall employee satisfaction is around {metrics['Satisfaction %']}%. "
        f"While positives highlight {pos_feedback[0].lower()} and {pos_feedback[1].lower()}, "
        f"negatives such as {neg_feedback[0].lower()} remain areas of concern. "
        f"In an M&A context, this suggests {('a strong cultural foundation' if metrics['Satisfaction %'] > 75 else 'a need for deeper cultural due diligence')}."
    )

# ---------------------------
# PDF Export Function
# ---------------------------
def create_pdf(company, summary, metrics, pos_feedback, neg_feedback, highlights, insights):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"HR Due Diligence Report - {company}", ln=True, align="C")
    pdf.ln(10)

    pdf.multi_cell(0, 10, f"Executive Summary:\n{summary}")
    pdf.ln(5)

    pdf.cell(200, 10, txt="Key HR Metrics", ln=True)
    for k, v in metrics.items():
        pdf.cell(200, 10, txt=f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Employee Feedback", ln=True)
    pdf.multi_cell(0, 10, "Positive:\n- " + "\n- ".join(pos_feedback))
    pdf.multi_cell(0, 10, "Negative:\n- " + "\n- ".join(neg_feedback))

    pdf.ln(5)
    pdf.cell(200, 10, txt="Highlights", ln=True)
    for h in highlights:
        pdf.multi_cell(0, 10, f"- {h}")

    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Insights & Recommendations:\n{insights}")

    return pdf.output(dest="S").encode("latin-1")

# ---------------------------
# Streamlit Layout
# ---------------------------
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

company = st.text_input("Enter Company Name", value="").strip()

if company:
    if company in company_data:
        data = company_data[company]
        summary = data["summary"]
        metrics = data["metrics"]
        pos_feedback = data["feedback_positive"]
        neg_feedback = data["feedback_negative"]
        highlights = data["highlights"]
        culture_keywords = data["culture_keywords"]
    else:
        summary = generate_summary(company)
        metrics = generate_metrics()
        pos_feedback, neg_feedback = generate_feedback()
        highlights = generate_highlights()
        culture_keywords = generate_culture_keywords()

    # Executive Summary
    st.subheader("Executive Summary")
    st.write(summary)

    # Key HR Metrics
    st.subheader("Key HR Metrics")
    metric_cols = st.columns(len(metrics))
    for i, (k, v) in enumerate(metrics.items()):
        metric_cols[i].metric(k, v)

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
    st.subheader("Key Highlights")
    for h in highlights:
        st.markdown(f"- {h}")

    # Insights
    st.subheader("Insights & Recommendations")
    insights = generate_insights(summary, metrics, pos_feedback, neg_feedback)
    st.write(insights)

    # Culture Word Cloud
    st.subheader("Culture & Sentiment Word Cloud")
    fig, ax = plt.subplots(figsize=(10, 4))
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(culture_keywords)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Download buttons
    st.subheader("Download Report")
    pdf_bytes = create_pdf(company, summary, metrics, pos_feedback, neg_feedback, highlights, insights)
    st.download_button("Download as PDF", pdf_bytes, file_name=f"{company}_HR_Report.pdf", mime="application/pdf")

    txt_report = f"Executive Summary:\n{summary}\n\nMetrics:\n{metrics}\n\nPositive Feedback:\n{pos_feedback}\n\nNegative Feedback:\n{neg_feedback}\n\nHighlights:\n{highlights}\n\nInsights:\n{insights}"
    st.download_button("Download as TXT", txt_report, file_name=f"{company}_HR_Report.txt")
else:
    st.info("Please enter a company name to generate the HR report.")

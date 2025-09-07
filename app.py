import streamlit as st
import pandas as pd
import random
import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from fpdf import FPDF

# ---------------------------
# Load Company Data
# ---------------------------
def load_company_data():
    try:
        with open("sample_reviews.json", "r") as f:
            return json.load(f)
    except Exception:
        return {}

COMPANY_DB = load_company_data()

# ---------------------------
# Fallback Generators
# ---------------------------
def generate_summary(company):
    strengths = ["supportive management", "flexible work hours", "innovative culture", "strong training programs", "team collaboration", "diverse teams"]
    weaknesses = ["slow decision-making", "limited recognition", "high workload", "training gaps", "internal politics", "inconsistent policies"]
    culture_aspects = ["team collaboration", "innovation-driven environment", "continuous learning", "employee engagement programs"]

    return (
        f"{company} has several strengths including {random.choice(strengths)} and {random.choice(strengths)}. "
        f"The company culture emphasizes {random.choice(culture_aspects)}. "
        f"Areas for improvement include {random.choice(weaknesses)} and {random.choice(weaknesses)}. "
        f"Employee sentiment appears {'generally positive' if random.random() > 0.3 else 'mixed'}, with feedback highlighting both achievements and challenges. "
        f"Overall, {company} presents an environment where employees experience growth opportunities while facing some operational challenges."
    )

def generate_metrics():
    return {
        "Average Tenure (years)": round(random.uniform(2, 8), 1),
        "Annual Attrition Rate (%)": round(random.uniform(8, 25), 1),
        "Engagement Score (/5)": round(random.uniform(3, 5), 1),
        "Glassdoor Rating (/5)": round(random.uniform(3, 5), 1),
        "Satisfaction %": random.randint(60, 95)
    }

def generate_feedback():
    positive = [
        "Supportive team culture",
        "Opportunities to learn",
        "Good work-life balance",
        "Flexible hours",
        "Strong leadership",
        "Mentorship programs",
        "Inclusive environment"
    ]
    negative = [
        "High workload pressure",
        "Limited recognition",
        "Slow decision-making",
        "Training gaps",
        "Internal politics",
        "Inconsistent policies",
        "Promotion delays"
    ]
    return random.sample(positive, k=4), random.sample(negative, k=4)

def generate_highlights():
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
    keywords = ["Innovation", "Collaboration", "Integrity", "Learning", "Accountability", "Diversity", "Empathy", "Agility", "Trust", "Communication"]
    return {k: random.randint(5, 20) for k in keywords}

# ---------------------------
# Generate Insights
# ---------------------------
def generate_insights(summary, metrics, pos_feedback, neg_feedback):
    satisfaction = metrics.get("Satisfaction %", round(metrics.get("Engagement Score (/5)", 3.5) * 20))

    insights = [
        f"Based on available reviews, the overall employee satisfaction is around {satisfaction}%.",
        f"Attrition rate stands at {metrics.get('Annual Attrition Rate (%)', 'N/A')}%, indicating {'stable retention' if metrics.get('Annual Attrition Rate (%)', 15) < 15 else 'possible retention challenges'}.",
        f"Key positive aspects include {', '.join(pos_feedback[:2])}.",
        f"However, employees often raise concerns about {', '.join(neg_feedback[:2])}.",
        "Overall, the organization presents a balanced outlook with clear strengths and some improvement areas."
    ]
    return insights

# ---------------------------
# PDF Export
# ---------------------------
def create_pdf(company, summary, metrics, pos_feedback, neg_feedback, highlights, insights):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"HR Due Diligence Report: {company}", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, f"\nExecutive Summary:\n{summary}")

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Key HR Metrics:", ln=True)
    pdf.set_font("Arial", "", 12)
    for k, v in metrics.items():
        pdf.cell(0, 10, f"- {k}: {v}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Positive Feedback:", ln=True)
    pdf.set_font("Arial", "", 12)
    for f in pos_feedback:
        pdf.cell(0, 10, f"- {f}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Negative Feedback:", ln=True)
    pdf.set_font("Arial", "", 12)
    for f in neg_feedback:
        pdf.cell(0, 10, f"- {f}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Highlights:", ln=True)
    pdf.set_font("Arial", "", 12)
    for h in highlights:
        pdf.cell(0, 10, f"- {h}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Insights:", ln=True)
    pdf.set_font("Arial", "", 12)
    for i in insights:
        pdf.multi_cell(0, 10, f"- {i}")

    return pdf.output(dest="S").encode("latin-1")

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

company = st.text_input("Enter Company Name", value="").strip()

if company:
    data = COMPANY_DB.get(company)

    if data:  # Use JSON data
        summary = data["summary"]
        metrics = data["metrics"]
        pos_feedback = data["positive_feedback"]
        neg_feedback = data["negative_feedback"]
        highlights = data["highlights"]
    else:  # Fallback to random
        summary = generate_summary(company)
        metrics = generate_metrics()
        pos_feedback, neg_feedback = generate_feedback()
        highlights = generate_highlights()

    insights = generate_insights(summary, metrics, pos_feedback, neg_feedback)

    # Executive Summary
    st.subheader("Executive Summary")
    st.write(summary)

    # HR Metrics
    st.subheader("Key HR Metrics")
    metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
    st.dataframe(metrics_df, use_container_width=True)

    # Feedback
    st.subheader("Employee Feedback")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Positive Feedback**")
        for f in pos_feedback:
            st.markdown(f"- {f}")
    with col2:
        st.markdown("**Negative Feedback**")
        for f in neg_feedback:
            st.markdown(f"- {f}")

    # Highlights
    st.subheader("Key Highlights")
    for h in highlights:
        st.markdown(f"- {h}")

    # Insights
    st.subheader("Consultant Insights / Conclusion")
    for i in insights:
        st.markdown(f"- {i}")

    # Culture Word Cloud (last)
    st.subheader("Culture & Sentiment (Word Cloud)")
    culture_keywords = generate_culture_keywords()
    fig, ax = plt.subplots(figsize=(8, 4))
    wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(culture_keywords)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # Download PDF
    pdf_bytes = create_pdf(company, summary, metrics, pos_feedback, neg_feedback, highlights, insights)
    st.download_button("📥 Download Full Report (PDF)", data=pdf_bytes, file_name=f"{company}_HR_Report.pdf", mime="application/pdf")

else:
    st.info("Please enter a company name to generate the HR report.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json
from fpdf import FPDF

# ---------------------------
# Load sample reviews JSON
# ---------------------------
with open("sample_reviews.json", "r") as f:
    company_data = json.load(f)

companies = sorted(company_data.keys())

# ---------------------------
# Streamlit Layout
# ---------------------------
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

# Company dropdown
company = st.selectbox("Select Company", companies)

if company:
    data = company_data[company]
    summary = data["summary"]
    metrics = data["metrics"]
    pos_feedback = data["positive_feedback"]
    neg_feedback = data["negative_feedback"]
    highlights = data["highlights"]

    # Executive Summary
    st.subheader("Executive Summary")
    st.write(summary)

    # Key HR Metrics Table with conditional formatting
    st.subheader("Key HR Metrics")
    metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])

    def color_metrics(val):
        if isinstance(val, (int, float)):
            if val > 80 or val > 4.5:  # high values
                return 'background-color: #b6fcb6'  # light green
            elif val < 60 or val < 3.5:  # low values
                return 'background-color: #ffb3b3'  # light red
        return ''
    st.dataframe(metrics_df.style.applymap(color_metrics, subset=["Value"]), height=200)

    # Employee Feedback
    st.subheader("Employee Feedback")
    fb_col1, fb_col2 = st.columns(2)
    fb_col1.markdown("**Positive Feedback**")
    for f in pos_feedback:
        fb_col1.markdown(f"- {f}")
    fb_col2.markdown("**Negative Feedback**")
    for f in neg_feedback:
        fb_col2.markdown(f"- {f}")

    # Highlights / Key Insights
    st.subheader("Key Insights / Highlights")
    for h in highlights:
        st.markdown(f"- {h}")

    # Culture Word Cloud at the bottom
    st.subheader("Culture & Sentiment")
    keywords = ["Innovation", "Collaboration", "Integrity", "Learning", "Accountability",
                "Diversity", "Empathy", "Agility", "Trust", "Communication"]
    word_freq = {k: metrics.get("Satisfaction %", 10) + (i*2) for i, k in enumerate(keywords)}
    fig, ax = plt.subplots(figsize=(10,4))
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

    # PDF Download
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"HR Due Diligence Report - {company}", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, "Executive Summary:")
        pdf.multi_cell(0, 8, summary)
        pdf.ln(5)

        pdf.cell(0, 8, "Key HR Metrics:", ln=True)
        for m, v in metrics.items():
            pdf.cell(0, 8, f"{m}: {v}", ln=True)
        pdf.ln(5)

        pdf.cell(0, 8, "Positive Feedback:", ln=True)
        for f in pos_feedback:
            pdf.cell(0, 8, f"- {f}", ln=True)
        pdf.ln(5)

        pdf.cell(0, 8, "Negative Feedback:", ln=True)
        for f in neg_feedback:
            pdf.cell(0, 8, f"- {f}", ln=True)
        pdf.ln(5)

        pdf.cell(0, 8, "Key Highlights:", ln=True)
        for h in highlights:
            pdf.cell(0, 8, f"- {h}", ln=True)

        pdf_file = f"{company}_HR_Report.pdf"
        pdf.output(pdf_file)
        return pdf_file

    if st.button("Download Report as PDF"):
        pdf_file = create_pdf()
        with open(pdf_file, "rb") as f:
            st.download_button("Click here to download PDF", f, file_name=pdf_file)

else:
    st.info("Please select a company from the dropdown to generate the HR report.")

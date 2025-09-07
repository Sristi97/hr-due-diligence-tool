import streamlit as st
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
companies.insert(0, "Select a company...")  # Default placeholder

# ---------------------------
# Streamlit Layout
# ---------------------------
st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

# Company dropdown
company = st.selectbox("Select Company", companies)

# ---------------------------
# Function to generate multi-paragraph summary
# ---------------------------
def generate_long_summary(company, data):
    summary = f"**{company} Executive Summary**\n\n"
    summary += f"{data['summary']}\n\n"
    
    # Paragraph on positive aspects
    pos_str = ", ".join(data['positive_feedback'])
    summary += f"Employees highlight the following strengths: {pos_str}. These contribute to a collaborative and engaging work environment.\n\n"
    
    # Paragraph on challenges
    neg_str = ", ".join(data['negative_feedback'])
    summary += f"Areas for improvement include: {neg_str}. Addressing these can improve employee satisfaction and reduce attrition risks.\n\n"
    
    # Paragraph on highlights
    highlights_str = " ".join(data['highlights'])
    summary += f"Key observations from employee feedback and HR metrics indicate: {highlights_str}\n\n"
    
    # Optional recommendation paragraph
    summary += "Overall, the company presents growth opportunities while facing operational challenges. Focus on recognition, workload management, and engagement initiatives is recommended."
    
    return summary

# ---------------------------
# Render report only if a company is selected
# ---------------------------
if company != "Select a company...":
    data = company_data[company]
    summary = generate_long_summary(company, data)
    metrics = data["metrics"]
    pos_feedback = data["positive_feedback"]
    neg_feedback = data["negative_feedback"]
    highlights = data["highlights"]

    # Executive Summary
    st.subheader("Executive Summary")
    st.write(summary)

    # Key HR Metrics as cards
    st.subheader("Key HR Metrics")
    metric_cols = st.columns(len(metrics))
    for i, (metric, value) in enumerate(metrics.items()):
        with metric_cols[i]:
            st.metric(label=metric, value=value)

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

import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
from io import BytesIO

# ---------------------------
# Dummy Data Generators
# ---------------------------

def generate_summary(company):
    sentiment_score = random.random()
    
    if "tech" in company.lower():
        strengths = ["innovation-driven projects", "continuous learning", "modern technology stack", "collaborative teams"]
        weaknesses = ["rapid changes can cause confusion", "tight deadlines", "long hours during sprints"]
        culture_aspects = ["innovation-focused environment", "agile methodologies", "peer learning culture"]
    elif "consult" in company.lower():
        strengths = ["strong teamwork", "client-centric approach", "structured processes", "mentorship programs"]
        weaknesses = ["high workload", "slow decision-making", "internal politics"]
        culture_aspects = ["collaborative environment", "client engagement focus", "knowledge sharing culture"]
    else:
        strengths = ["supportive management", "flexible work hours", "employee engagement programs", "diverse teams"]
        weaknesses = ["limited recognition", "inconsistent policies", "training gaps", "high workload"]
        culture_aspects = ["team collaboration", "continuous learning", "inclusive culture"]

    summary = (
        f"{company} has several strengths including {random.choice(strengths)} and {random.choice(strengths)}. "
        f"The company culture emphasizes {random.choice(culture_aspects)}. "
        f"Areas for improvement include {random.choice(weaknesses)} and {random.choice(weaknesses)}. "
        f"Employee sentiment appears {'generally positive' if sentiment_score > 0.6 else 'mixed'}, "
        f"highlighting both achievements and challenges. Overall, {company} presents an environment "
        f"where employees experience growth opportunities while facing some operational challenges."
    )
    return summary, sentiment_score

def generate_metrics(sentiment_score):
    return {
        "Number of Reviews": random.randint(50, 500),
        "Attrition %": round((1-sentiment_score)*20 + 5, 1),
        "Average Tenure (yrs)": round(random.uniform(1, 10), 1),
        "Satisfaction %": int(sentiment_score*35 + 60),
        "Overall Rating": round(sentiment_score*2.0 + 3.0, 1)
    }

def generate_feedback(sentiment_score):
    positive_feedback = [
        "Supportive team culture",
        "Opportunities to learn",
        "Good work-life balance",
        "Flexible hours",
        "Strong leadership",
        "Mentorship programs",
        "Inclusive environment"
    ]
    negative_feedback = [
        "High workload pressure",
        "Limited recognition",
        "Slow decision-making",
        "Training gaps",
        "Internal politics",
        "Inconsistent policies",
        "Promotion delays"
    ]
    pos_count = 4 if sentiment_score > 0.6 else 2
    neg_count = 2 if sentiment_score > 0.6 else 4
    
    pos = random.sample(positive_feedback, k=pos_count)
    neg = random.sample(negative_feedback, k=neg_count)
    return pos, neg

def generate_culture_keywords(sentiment_score):
    keywords = ["Innovation", "Collaboration", "Integrity", "Learning", "Accountability",
                "Diversity", "Empathy", "Agility", "Trust", "Communication"]
    word_freq = {k: int(random.randint(5,20)*sentiment_score if i%2==0 else random.randint(5,20)*(1-sentiment_score)) 
                 for i,k in enumerate(keywords)}
    return word_freq

def generate_highlights(sentiment_score):
    highlights = [
        "Employees appreciate collaborative work environment.",
        "Training programs are improving but still limited in reach.",
        "Management is supportive but decision-making can be slow.",
        "Work-life balance is rated highly among teams.",
        "Recognition programs are not consistent across departments.",
        "Innovation is encouraged but execution is sometimes delayed.",
        "Team engagement initiatives are increasing employee satisfaction."
    ]
    return random.sample(highlights, k=4)

def generate_insights(metrics, pos_feedback, neg_feedback):
    insights = []
    if metrics["Attrition %"] > 15:
        insights.append("High attrition observed; retention strategies should be reviewed.")
    else:
        insights.append("Attrition is within normal range.")
    
    if metrics["Satisfaction %"] < 75:
        insights.append("Employee satisfaction is moderate; consider engagement initiatives.")
    else:
        insights.append("Employee satisfaction is strong.")
    
    if len(pos_feedback) > len(neg_feedback):
        insights.append("Positive feedback outweighs negative feedback; culture seems healthy.")
    else:
        insights.append("Negative feedback is significant; cultural and operational improvements recommended.")
    
    return insights

# ---------------------------
# Streamlit Layout
# ---------------------------

st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

company = st.text_input("Enter Company Name", value="").strip()

if company:
    # Generate dynamic data
    summary, sentiment_score = generate_summary(company)
    metrics = generate_metrics(sentiment_score)
    pos_feedback, neg_feedback = generate_feedback(sentiment_score)
    culture_keywords = generate_culture_keywords(sentiment_score)
    highlights = generate_highlights(sentiment_score)
    insights = generate_insights(metrics, pos_feedback, neg_feedback)
    
    # Executive Summary
    st.subheader("Executive Summary")
    st.write(summary)
    
    # Key HR Metrics as Cards
    st.subheader("Key HR Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Number of Reviews", metrics["Number of Reviews"])
    col2.metric("Attrition %", f"{metrics['Attrition %']}%", delta="High" if metrics['Attrition %']>15 else "OK")
    col3.metric("Average Tenure", f"{metrics['Average Tenure (yrs)']} yrs")
    col4.metric("Satisfaction %", f"{metrics['Satisfaction %']}%", delta="Low" if metrics['Satisfaction %']<75 else "Good")
    col5.metric("Overall Rating", metrics["Overall Rating"])
    
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
    
    # Insights / Recommendations
    st.subheader("Insights & Recommendations")
    for insight in insights:
        st.markdown(f"- {insight}")
    
    # Culture Word Cloud at the end
    st.subheader("Culture & Sentiment Word Cloud")
    fig, ax = plt.subplots(figsize=(10,4))
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(culture_keywords)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
    
    # Downloadable TXT Report
    st.subheader("Download Report")
    report_text = f"Company: {company}\n\nSummary:\n{summary}\n\nMetrics:\n" \
                  f"{pd.DataFrame(metrics.items(), columns=['Metric','Value']).to_string(index=False)}\n\n" \
                  f"Positive Feedback: {pos_feedback}\nNegative Feedback: {neg_feedback}\n\n" \
                  f"Highlights: {highlights}\n\nInsights: {insights}"
    st.download_button("Download Report as TXT", report_text, file_name=f"{company}_HR_Report.txt")
    
    # Download PDF Report
    pdf_btn = st.button("Download Report as PDF")
    if pdf_btn:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"HR Due Diligence Report: {company}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.ln(5)
        
        # Summary
        pdf.multi_cell(0, 8, f"Executive Summary:\n{summary}")
        pdf.ln(5)
        
        # Metrics
        pdf.multi_cell(0, 8, "Key HR Metrics:")
        for k,v in metrics.items():
            pdf.multi_cell(0, 8, f"{k}: {v}")
        pdf.ln(3)
        
        # Feedback
        pdf.multi_cell(0, 8, f"Positive Feedback: {', '.join(pos_feedback)}")
        pdf.multi_cell(0, 8, f"Negative Feedback: {', '.join(neg_feedback)}")
        pdf.ln(3)
        
        # Highlights
        pdf.multi_cell(0, 8, f"Highlights: {', '.join(highlights)}")
        pdf.ln(3)
        
        # Insights
        pdf.multi_cell(0, 8, f"Insights & Recommendations: {', '.join(insights)}")
        pdf.ln(3)
        
        # Save PDF to BytesIO and provide download
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        st.download_button("Download PDF Report", pdf_buffer, file_name=f"{company}_HR_Report.pdf")

else:
    st.info("Please enter a company name to generate the HR report.")

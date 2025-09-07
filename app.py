import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------
# Dummy Data Generators
# ---------------------------

def generate_summary(company):
    strengths = ["supportive management", "flexible work hours", "innovative culture", "strong training programs", "team collaboration", "diverse teams"]
    weaknesses = ["slow decision-making", "limited recognition", "high workload", "training gaps", "internal politics", "inconsistent policies"]
    culture_aspects = ["team collaboration", "innovation-driven environment", "continuous learning", "employee engagement programs"]
    
    summary = (
        f"{company} has several strengths including {random.choice(strengths)} and {random.choice(strengths)}. "
        f"The company culture emphasizes {random.choice(culture_aspects)}. "
        f"Areas for improvement include {random.choice(weaknesses)} and {random.choice(weaknesses)}. "
        f"Employee sentiment appears {'generally positive' if random.random() > 0.3 else 'mixed'}, with feedback highlighting both achievements and challenges. "
        f"Overall, {company} presents an environment where employees experience growth opportunities while facing some operational challenges."
    )
    return summary

def generate_metrics():
    return {
        "Number of Reviews": random.randint(50, 500),
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
    pos = random.sample(positive_feedback, k=4)
    neg = random.sample(negative_feedback, k=4)
    return pos, neg

def generate_culture_keywords():
    keywords = ["Innovation", "Collaboration", "Integrity", "Learning", "Accountability", "Diversity", "Empathy", "Agility", "Trust", "Communication"]
    word_freq = {k: random.randint(5,20) for k in random.sample(keywords, k=len(keywords))}
    return word_freq

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
    return random.sample(highlights, k=4)

# ---------------------------
# Streamlit Layout
# ---------------------------

st.set_page_config(page_title="HR Due Diligence Dashboard", layout="wide")
st.title("HR Due Diligence Dashboard")

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
    
    # Key Metrics Table
    st.subheader("Key HR Metrics")
    metrics_df = pd.DataFrame(metrics.items(), columns=["Metric", "Value"])
    st.table(metrics_df)
    
    # Employee Feedback in two columns
    st.subheader("Employee Feedback")
    fb_col1, fb_col2 = st.columns(2)
    fb_col1.markdown("**Positive Feedback**")
    for f in pos_feedback:
        fb_col1.markdown(f"- {f}")
    fb_col2.markdown("**Negative Feedback**")
    for f in neg_feedback:
        fb_col2.markdown(f"- {f}")
    
    # Feedback Bar Chart
    st.subheader("Feedback Overview")
    feedback_counts = pd.DataFrame({
        "Type": ["Positive", "Negative"],
        "Count": [len(pos_feedback), len(neg_feedback)]
    })
    st.bar_chart(feedback_counts.set_index("Type"))
    
    # Highlights
    st.subheader("Key Insights / Highlights")
    for h in highlights:
        st.markdown(f"- {h}")
    
    # Culture / Word Cloud at the bottom
    st.subheader("Culture & Sentiment")
    fig, ax = plt.subplots(figsize=(10,4))
    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(culture_keywords)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
    
else:
    st.info("Please enter a company name to generate the HR report.")

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
    

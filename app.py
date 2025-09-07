import streamlit as st
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------
# Dummy Data Generators
# ---------------------------

def generate_summary(company):
    # Determine sentiment score to tie metrics & summary
    sentiment_score = random.random()
    
    # Tailor strengths based on company name
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
        f"The company culture emphasizes {random.choice(culture_asp_

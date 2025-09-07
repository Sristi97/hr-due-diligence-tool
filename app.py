import json
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# -----------------------
# App Config
# -----------------------
st.set_page_config(page_title="HR Due Diligence Tool", layout="wide")
st.title("HR Due Diligence Dashboard")

# -----------------------
# Load Sample JSON
# -----------------------
sample_file = "sample_reviews.json"

try:
    with open(sample_file, "r") as f:
        data = json.load(f)
except Exception as e:
    st.error(f"Could not load sample JSON: {e}")
    data = {}

# -----------------------
# Input: Company Selection
# -----------------------
company_name = st.selectbox("Select Company", list(data.keys()))

company_data = data.get(company_name, {})

# -----------------------
# Display News
# -----------------------
st.subheader("News / Updates")
news = company_data.get("news", {}).get("data", [])
if news:
    for item in news:
        st.markdown(f"**{item.get('title', 'No Title')}**")
        st.write(item.get("description", "No Description"))
else:
    st.write("No news available.")

# -----------------------
# Display Google Snippets
# -----------------------
st.subheader("Google Snippets")
google_snippets = company_data.get("google_snippets", {"message": "No data available"})
st.json(google_snippets)

# -----------------------
# Display Reputation
# -----------------------
st.subheader("Reputation / Reviews")
reputation = company_data.get("reputation", {})
st.json(reputation)

# -----------------------
# Word Cloud: Culture / Sentiment
# -----------------------
st.subheader("Culture / Sentiment Word Cloud")

# Combine all text available in news + reputation for word cloud
text_for_wordcloud = ""
for item in news:
    text_for_wordcloud += " " + item.get("title", "") + " " + item.get("description", "")

# Add reputation texts if available
for key, value in reputation.items():
    text_for_wordcloud += " " + " ".join(str(v) for v in value.values())

if not text_for_wordcloud.strip():
    text_for_wordcloud = "Work culture Employee engagement HR satisfaction Benefits Leadership Teamwork Innovation"

wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_for_wordcloud)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# -----------------------
# Display Raw JSON Data
# -----------------------
st.subheader("Raw JSON Data")
st.json(company_data)

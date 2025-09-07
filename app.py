import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

NEWS_API_KEY = os.environ.get("NEWSDATA_API_KEY")
if not NEWS_API_KEY:
    raise ValueError("Please set the NEWSDATA_API_KEY environment variable")

# Fetch news for a company
def fetch_news(company):
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={company}&language=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "results" not in data or len(data["results"]) == 0:
            return None
        return data["results"]
    except Exception:
        return None

# Fetch Google snippets (simple search results)
def fetch_google_snippets(company):
    try:
        search_url = f"https://www.google.com/search?q={company}+company+review"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        # Minimal parsing for demonstration
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        snippets = [s.get_text() for s in soup.select("span.aCOpRe")]
        return snippets[:5] if snippets else None
    except Exception:
        return None

@app.route("/api/company/<company>", methods=["GET"])
def api_company(company):
    news_data = fetch_news(company)
    google_snippets = fetch_google_snippets(company)

    # Fallback JSON if nothing available
    if not news_data and not google_snippets:
        return jsonify({
            "company": company,
            "news": [],
            "google_snippets": [],
            "message": "No data available for this company"
        }), 200

    return jsonify({
        "company": company,
        "news": news_data or [],
        "google_snippets": google_snippets or []
    }), 200

if __name__ == "__main__":
    app.run(debug=True)

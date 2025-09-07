#!/usr/bin/env python3
"""
generate_sample_reviews.py
Generates sample_reviews.json from a companies.txt list.
Outputs JSON entries that match the app's expected schema.
"""

import json
import random
import argparse
from pathlib import Path

# ---------------------------
# Helpers & Templates
# ---------------------------
INDUSTRY_TEMPLATES = {
    "tech": {
        "strengths": ["innovation-driven projects", "cutting-edge tech", "strong R&D", "flexible/hybrid work"],
        "weaknesses": ["tight deadlines", "rapid reorgs", "high performance pressure", "long hours during sprints"],
        "culture": ["innovation", "continuous learning", "peer collaboration", "agile ways of working"],
        "pos": ["Great learning opportunities", "Modern tech stack", "Flexible work policies", "Strong peer culture"],
        "neg": ["Workload can be high", "Frequent reorganizations", "Performance pressure", "Siloed teams"],
        "highlights": ["High innovation focus", "Attracts top talent", "Fast product cycles"]
    },
    "consulting_it": {
        "strengths": ["structured training and career paths", "client exposure", "global delivery", "mentorship programs"],
        "weaknesses": ["project-driven workload spikes", "billable-pressure", "slow promotions in some bands"],
        "culture": ["client-first mindset", "knowledge sharing", "process orientation"],
        "pos": ["Strong training", "Global opportunities", "Career development", "Structured processes"],
        "neg": ["Work-life varies by project", "Billable targets", "Travel requirements"],
        "highlights": ["Good for career growth", "Excellent learning programs"]
    },
    "finance": {
        "strengths": ["strong compliance and process", "financial stability", "clear career ladders"],
        "weaknesses": ["conservative culture", "bureaucracy", "long hours in investment banking roles"],
        "culture": ["risk-aware", "process-driven", "client-focused"],
        "pos": ["Good compensation", "Clear processes", "Professional environment"],
        "neg": ["Conservative decision-making", "High stress in deal teams"],
        "highlights": ["Strong brand in finance", "Robust compliance"]
    },
    "pharma_health": {
        "strengths": ["research-led culture", "strong benefits", "stable career paths"],
        "weaknesses": ["slow decision-making", "regulatory constraints", "gradual career progression"],
        "culture": ["evidence-driven", "collaborative R&D", "patient-centric"],
        "pos": ["Strong benefits", "Meaningful work", "Stable roles"],
        "neg": ["Slow promotions", "Bureaucratic processes"],
        "highlights": ["High R&D investment", "Strong employer brand for stability"]
    },
    "retail_consumer": {
        "strengths": ["scale and distribution", "brand recognition", "fast operational execution"],
        "weaknesses": ["hourly workforce issues", "margin pressures", "variable scheduling"],
        "culture": ["customer-centric", "operationally focused", "fast turnaround"],
        "pos": ["Great brand", "Many entry-level opportunities", "Strong logistics"],
        "neg": ["Work-life scheduling challenges", "Pressure on margins", "Seasonal spikes"],
        "highlights": ["High brand pull", "Operational excellence"]
    },
    "auto": {
        "strengths": ["engineering heritage", "scale manufacturing", "global supply chains"],
        "weaknesses": ["legacy processes", "slow product cycles", "union/HR complexities"],
        "culture": ["engineering-driven", "safety-first", "manufacturing discipline"],
        "pos": ["Strong engineering teams", "Stable manufacturing roles"],
        "neg": ["Legacy processes", "Slow change"],
        "highlights": ["Large-scale manufacturing capabilities"]
    },
    "energy": {
        "strengths": ["scale and capital", "global reach", "stable demand"],
        "weaknesses": ["regulatory complexity", "safety/regulatory constraints", "legacy systems"],
        "culture": ["safety-first", "regulation-aware", "operational continuity"],
        "pos": ["Stable careers", "Strong safety programs"],
        "neg": ["Slow tech adoption in some pockets"],
        "highlights": ["Capital-intensive operations"]
    },
    "telecom": {
        "strengths": ["large customer base", "infrastructure scale", "regulated cash flows"],
        "weaknesses": ["competitive pressures", "legacy networks", "regulatory oversight"],
        "culture": ["operations-driven", "customer-centric", "infrastructure-heavy"],
        "pos": ["Stable demand", "Network scale"],
        "neg": ["Legacy tech", "Regulatory complexity"],
        "highlights": ["Large-scale infrastructure operations"]
    },
    "industrial": {
        "strengths": ["engineering excellence", "long-term contracts", "diverse product lines"],
        "weaknesses": ["cyclical demand", "supply-chain sensitivity"],
        "culture": ["engineering-focused", "safety-first", "process-driven"],
        "pos": ["Reliable products", "Skilled workforce"],
        "neg": ["Cyclicality effects", "Sourcing challenges"],
        "highlights": ["Strong industrial heritage"]
    },
    "media_entertainment": {
        "strengths": ["creative talent", "brand reach", "content portfolio"],
        "weaknesses": ["cyclical revenues", "creative churn", "reorgs"],
        "culture": ["creative", "deadline-driven", "high collaboration"],
        "pos": ["Creative work", "Brand recognition"],
        "neg": ["High project stress", "Reorganizations"],
        "highlights": ["High audience reach"]
    },
    "ecommerce": {
        "strengths": ["digital-first", "data-driven", "fast execution"],
        "weaknesses": ["logistics complexity", "margin pressure", "customer service load"],
        "culture": ["data-driven", "fast-paced", "customer-obsessed"],
        "pos": ["Fast growth", "Data-driven insights"],
        "neg": ["Logistics & returns stress", "Burnout in operations"],
        "highlights": ["Rapid growth environment"]
    },
    "default": {
        "strengths": ["supportive management", "diverse teams", "learning opportunities"],
        "weaknesses": ["process gaps", "limited recognition", "training gaps"],
        "culture": ["collaboration", "continuous learning"],
        "pos": ["Supportive teams", "Learning culture"],
        "neg": ["Inconsistent policies", "Training gaps"],
        "highlights": ["Balanced profile"]
    }
}

# ---------------------------
# Industry detection heuristics
# ---------------------------
def detect_industry(name):
    n = name.lower()
    if any(k in n for k in ("software","tech","nvidia","intel","microsoft","google","meta","amazon","apple","oracle","ibm","adobe","salesforce","cisco","sap","tencent","alibaba","baidu","bytedance","xiaomi","huawei")):
        return "tech"
    if any(k in n for k in ("consult","accenture","capgemini","cognizant","tcs","infosys","wipro","hcl","eci")):
        return "consulting_it"
    if any(k in n for k in ("bank","jpmorgan","goldman","hsbc","bank of","barclays","citigroup","wells","ubs","credit","santander","deutsche")):
        return "finance"
    if any(k in n for k in ("pharma","pfizer","novartis","roche","merck","glaxo","sanofi","astrazeneca","j&j","johnson","health")):
        return "pharma_health"
    if any(k in n for k in ("walmart","costco","retail","target","tesco","carrefour","kroger","mcdonald","starbucks","kfc","yum","nike","adidas","inditex","h&m","zara")):
        return "retail_consumer"
    if any(k in n for k in ("toyota","volkswagen","mercedes","bmw","honda","ford","general motors","gm","nissan","hyundai","mahindra","bajaj","tesla")):
        return "auto"
    if any(k in n for k in ("exxon","chevron","bp ","shell","total","petrochina","sinopec","saudi aramco","adani")):
        return "energy"
    if any(k in n for k in ("verizon","at&t","telefonica","vodafone","telecom","china mobile","deutsche telekom")):
        return "telecom"
    if any(k in n for k in ("siemens","ge ","honeywell","3m","caterpillar","boeing","abb","schneider")):
        return "industrial"
    if any(k in n for k in ("comcast","disney","netflix","warner","paramount","viacom","sony pictures")):
        return "media_entertainment"
    if any(k in n for k in ("amazon","alibaba","jd","shopify","ebay","flipkart","rakuten","booking","uber","lyft")):
        return "ecommerce"
    # fallback
    return "default"

# ---------------------------
# Metric generation per industry
# ---------------------------
def gen_metrics_for_industry(industry):
    if industry == "tech":
        return {
            "Average Tenure (years)": round(random.uniform(2.5, 6.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(8, 20), 1),
            "Engagement Score (/5)": round(random.uniform(3.6, 4.8), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.5, 4.6), 1),
            "Satisfaction %": random.randint(70, 95)
        }
    if industry == "consulting_it":
        return {
            "Average Tenure (years)": round(random.uniform(2.0, 5.5), 1),
            "Annual Attrition Rate (%)": round(random.uniform(10, 22), 1),
            "Engagement Score (/5)": round(random.uniform(3.5, 4.5), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.4, 4.4), 1),
            "Satisfaction %": random.randint(65, 90)
        }
    if industry == "finance":
        return {
            "Average Tenure (years)": round(random.uniform(3.0, 8.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(6, 18), 1),
            "Engagement Score (/5)": round(random.uniform(3.4, 4.5), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.2, 4.3), 1),
            "Satisfaction %": random.randint(60, 88)
        }
    if industry == "pharma_health":
        return {
            "Average Tenure (years)": round(random.uniform(3.5, 8.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(6, 16), 1),
            "Engagement Score (/5)": round(random.uniform(3.6, 4.5), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.5, 4.4), 1),
            "Satisfaction %": random.randint(68, 92)
        }
    if industry == "retail_consumer":
        return {
            "Average Tenure (years)": round(random.uniform(1.5, 6.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(10, 35), 1),
            "Engagement Score (/5)": round(random.uniform(3.0, 4.3), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.0, 4.2), 1),
            "Satisfaction %": random.randint(50, 85)
        }
    if industry == "auto":
        return {
            "Average Tenure (years)": round(random.uniform(3.0, 9.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(6, 18), 1),
            "Engagement Score (/5)": round(random.uniform(3.4, 4.4), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.2, 4.2), 1),
            "Satisfaction %": random.randint(60, 88)
        }
    if industry == "energy":
        return {
            "Average Tenure (years)": round(random.uniform(4.0, 10.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(4, 14), 1),
            "Engagement Score (/5)": round(random.uniform(3.6, 4.4), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.4, 4.3), 1),
            "Satisfaction %": random.randint(65, 90)
        }
    if industry == "telecom":
        return {
            "Average Tenure (years)": round(random.uniform(3.0, 8.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(6, 20), 1),
            "Engagement Score (/5)": round(random.uniform(3.3, 4.2), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.2, 4.1), 1),
            "Satisfaction %": random.randint(60, 86)
        }
    if industry == "industrial":
        return {
            "Average Tenure (years)": round(random.uniform(4.0, 10.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(4, 15), 1),
            "Engagement Score (/5)": round(random.uniform(3.5, 4.4), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.3, 4.2), 1),
            "Satisfaction %": random.randint(65, 90)
        }
    if industry == "media_entertainment":
        return {
            "Average Tenure (years)": round(random.uniform(2.0, 6.0), 1),
            "Annual Attrition Rate (%)": round(random.uniform(8, 24), 1),
            "Engagement Score (/5)": round(random.uniform(3.5, 4.5), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.4, 4.3), 1),
            "Satisfaction %": random.randint(65, 90)
        }
    if industry == "ecommerce":
        return {
            "Average Tenure (years)": round(random.uniform(1.5, 5.5), 1),
            "Annual Attrition Rate (%)": round(random.uniform(10, 30), 1),
            "Engagement Score (/5)": round(random.uniform(3.2, 4.4), 1),
            "Glassdoor Rating (/5)": round(random.uniform(3.1, 4.2), 1),
            "Satisfaction %": random.randint(55, 88)
        }
    # default
    return {
        "Average Tenure (years)": round(random.uniform(2.0, 7.0), 1),
        "Annual Attrition Rate (%)": round(random.uniform(6, 22), 1),
        "Engagement Score (/5)": round(random.uniform(3.2, 4.4), 1),
        "Glassdoor Rating (/5)": round(random.uniform(3.1, 4.4), 1),
        "Satisfaction %": random.randint(60, 90)
    }

# ---------------------------
# Item generator
# ---------------------------
def generate_entry(name):
    industry = detect_industry(name)
    template = INDUSTRY_TEMPLATES.get(industry, INDUSTRY_TEMPLATES["default"])

    # build summary
    summary = (
        f"{name} is known for {random.choice(template['strengths'])}. "
        f"The culture typically shows {random.choice(template['culture'])}. "
        f"Areas employees flag include {random.choice(template['weaknesses'])}. "
        f"Overall sentiment is {'generally positive' if random.random() > 0.4 else 'mixed'}, "
        f"with strengths around {random.choice(template['strengths'])} and development areas in operations."
    )

    metrics = gen_metrics_for_industry(industry)

    pos_pool = template["pos"]
    neg_pool = template["neg"]
    pos = random.sample(pos_pool, k=min(4, len(pos_pool)))
    neg = random.sample(neg_pool, k=min(4, len(neg_pool)))
    highlights = random.sample(template.get("highlights", ["Balanced profile"]), k= min(3, len(template.get("highlights", ["Balanced profile"]))))
    # culture keywords
    ck = {}
    possible_ck = template["culture"] + ["Trust", "Accountability", "Diversity", "Empathy", "Agility", "Communication"]
    for k in random.sample(possible_ck, k=min(6, len(possible_ck))):
        ck[k] = random.randint(6, 35)

    return {
        "summary": summary,
        "metrics": metrics,
        "positive_feedback": pos,
        "negative_feedback": neg,
        "highlights": highlights,
        "culture_keywords": ck
    }

# ---------------------------
# Main
# ---------------------------
def main(companies_file="companies.txt", out_file="sample_reviews.json", seed=None):
    if seed is not None:
        random.seed(seed)
    companies_path = Path(companies_file)
    if not companies_path.exists():
        print(f"ERROR: {companies_file} not found. Create it with one company name per line.")
        return

    names = [line.strip() for line in companies_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    print(f"Found {len(names)} companies in {companies_file}.")

    out = {}
    for name in names:
        out[name] = generate_entry(name)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"Generated {out_file} with {len(out)} entries.")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--companies", "-c", default="companies.txt", help="Path to companies list (one per line)")
    p.add_argument("--out", "-o", default="sample_reviews.json", help="Output JSON file")
    p.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = p.parse_args()
    main(companies_file=args.companies, out_file=args.out, seed=args.seed)

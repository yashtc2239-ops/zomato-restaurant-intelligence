# 🍕 Zomato Restaurant Intelligence
**End-to-End Data Analytics + Deployed Web Application | VIT Pune 3rd Year Portfolio**

**Author:** Yash Chavan | B.Tech CSE-DS | VIT Pune | 2024-28
**Live App:** [zomato-growth-navigator.streamlit.app](https://zomato-growth-navigator.streamlit.app)
**GitHub:** [yashtc2239-ops/zomato-restaurant-intelligence](https://github.com/yashtc2239-ops/zomato-restaurant-intelligence)

---

## 🚀 Live Demo

> **[→ Open Interactive Dashboard](https://zomato-growth-navigator.streamlit.app)**

4-page interactive dashboard with live filters, expansion scoring, and ML rating predictor — deployed on Streamlit Cloud.

---

## What This Project Is About

I analyzed 41,410+ Zomato restaurants in Bengaluru to answer one real business question — **where should Zomato expand next, and what actually drives restaurant ratings?**

This is not a tutorial project. Every phase was built around a specific business decision, not just "let's make charts." The final deliverable is a deployed, interactive web application — not just a notebook.

---

## Key Results

- Built a custom **Expansion Score algorithm** — Lavelle Road scored **95.6/100**, identified as the #1 expansion zone across 72 Bengaluru locations
- Random Forest model predicts restaurant ratings with **R² = 0.82** — outperforms Linear Regression by **179%**
- Discovered that **customer votes drive 69.3% of rating prediction** — 4.7x more important than price
- Table booking restaurants rate **0.52 points higher** and charge **2.6x more** (₹1,276 vs ₹482) — strongest binary quality signal
- Only **1.4% of 41,410 restaurants** achieve Excellent rating — a genuine market differentiator

---

## Project Phases

| Phase | What I Did | Output |
|-------|------------|--------|
| 1 | Defined business problem using MECE framework | Problem statement |
| 2 | Audited 2 Kaggle datasets — 51,717 rows, 17 columns | Schema audit report |
| 3 | ETL pipeline — cleaned to 41,410 rows, fixed dtypes, encoded features | `bengaluru_cleaned.csv` |
| 4 | EDA across 6 business questions | Statistical findings |
| 5 | 5 business-driven visualizations (Matplotlib + Seaborn) | 5 chart PNGs |
| 6 | 8 SQL queries on SQLite — expansion recommendation | `business_queries.sql` |
| 7 | 3-page Power BI dashboard with 5 DAX measures | `.pbix` dashboard |
| 8 | ML model + custom Expansion Score algorithm | R² = 0.82, Score report |
| 9 | Streamlit app + Docker containerization + Streamlit Cloud deployment | Live web app |

---

## Live App Features

- **Executive Overview** — 4 KPI cards, rating distribution, service donuts, cost vs quality chart
- **Location Intelligence** — Top/Bottom 10 locations, color-coded Expansion Priority table
- **Cuisine & Business** — Supply vs Quality analysis, Table Booking premium signal
- **ML Model Insights** — Feature importance, model comparison, **Live Rating Predictor**
- **Sidebar filters** — Filter by Location, Cuisine, Price Range, Min Rating — all charts update live

---

## Tools & Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python |
| Analysis | Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn |
| Database | SQLite (8 business queries) |
| Dashboard | Power BI Desktop (3 pages, 5 DAX measures) |
| Web App | Streamlit + Plotly |
| Deployment | Streamlit Cloud |
| Container | Docker |
| Version Control | Git / GitHub |

---

## ML Model Results

| Model | R² Score | RMSE | Verdict |
|-------|----------|------|---------|
| Linear Regression | 0.29 | 0.37 | Weak — linear assumption insufficient |
| **Random Forest** | **0.82** | **0.19** | **Winner — 179% better R²** |

**Top 5 features driving restaurant ratings:**

| Rank | Feature | Importance | Business Meaning |
|------|---------|------------|-----------------|
| 1 | Votes (engagement) | 69.3% | 4.7x more important than price |
| 2 | Cost for two | 14.7% | Price tier has moderate influence |
| 3 | Restaurant type | 10.9% | Format matters — fine dining rates highest |
| 4 | Online ordering | 3.0% | Minimal direct impact |
| 5 | Table booking | 2.1% | Low weight but confirms premium signal |

---

## Expansion Score Algorithm

```
Expansion Score = (40% × Demand Pressure) + (35% × Avg Rating) + (25% × Supply Gap)
```

All metrics normalized 0–100 using MinMaxScaler. Top 3 Critical zones:

| Location | Score | Priority | Restaurants | Avg Rating |
|----------|-------|----------|-------------|------------|
| Lavelle Road | 95.6 | 🔴 CRITICAL | 481 | 4.14 |
| Church Street | 91.1 | 🔴 CRITICAL | 546 | 3.99 |
| St. Marks Road | 81.6 | 🔴 CRITICAL | 343 | 4.02 |

---

## Business Recommendations

1. **Expand** in Lavelle Road, Church Street, St. Marks Road — Expansion Score > 80/100
2. **Redesign ranking algorithm** — weight engagement (votes) 4.7x higher than cost
3. **Target premium cuisine gap** — Modern Indian (4.31), European (4.26), Mediterranean (4.20) are underserved
4. **Scale table booking program** — 2.6x revenue potential per restaurant
5. **Quality programs** for Bommanahalli (3.19 avg) and RT Nagar (3.46 avg)

---

## Repository Structure

```
zomato-restaurant-intelligence/
│
├── app.py                        ← Streamlit web application (4 pages)
├── Dockerfile                    ← Container definition (7 annotated layers)
├── .dockerignore                 ← Excludes raw data & notebooks from image
├── requirements.txt              ← Pinned Python dependencies
├── packages.txt                  ← System packages for Streamlit Cloud
├── bengaluru_cleaned.csv         ← Processed dataset (41,410 restaurants)
│
├── .streamlit/
│   └── config.toml               ← Zomato red theme + server config
│
├── .devcontainer/
│   └── devcontainer.json         ← GitHub Codespaces config
│
├── notebooks/
│   ├── 00_dataset_audit.ipynb    ← Raw data audit & schema analysis
│   ├── 01_cleaning.ipynb         ← ETL pipeline & data cleaning
│   ├── 02_eda.ipynb              ← Exploratory data analysis
│   ├── 03_visualization.ipynb    ← Business-driven charts
│   ├── 04_sql_analysis.ipynb     ← 8 SQL business queries
│   └── 05_advanced_analysis.ipynb← ML model + Expansion Score
│
├── sql/
│   └── business_queries.sql      ← All SQL queries reference file
│
└── reports/
    ├── Phase8_Business_Report.pdf ← Full business analysis report
    ├── expansion_score.png        ← Expansion priority chart
    ├── feature_importance.png     ← ML feature importance chart
    ├── chart1_rating_distribution.png
    ├── chart2_table_booking.png
    ├── chart3_cost_vs_rating.png
    ├── chart4_location_rating.png
    └── chart5_cuisine_analysis.png
```

---

## Run Locally

```bash
# Clone the repo
git clone https://github.com/yashtc2239-ops/zomato-restaurant-intelligence.git
cd zomato-restaurant-intelligence

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Run with Docker

```bash
# Build image
docker build -t zomato-intelligence .

# Run container
docker run -p 8501:8501 zomato-intelligence

# Open browser
http://localhost:8501
```

---

## Dataset Source

- **Primary Dataset:** [Zomato Bengaluru Restaurants](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants)
  - This dataset was used for all phases, including data cleaning, exploratory data analysis, SQL querying, ML modeling, and the final web application deployment.

*Note: The raw data file is not included in this repository to comply with GitHub file size limits. Please download it from the Kaggle link above to run the project locally.*

---

*Built as 3rd year B.Tech CSE-DS portfolio project | VIT Pune | 2024-28*


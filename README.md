# Marketing Campaign Performance Analyzer

An interactive marketing analytics dashboard built with Python, Pandas, Streamlit, and Plotly to evaluate digital advertising performance and support data-driven marketing decisions.

## Project Overview

This project simulates the work of a marketing analyst evaluating digital campaign performance for a fictional e-commerce business, ShopSphere BD.

The dashboard analyzes 400 simulated marketing records across four advertising platforms to identify campaign performance trends, evaluate audience segments, and compare advertising efficiency.

## Key Features

- **Executive Overview:** Monitor advertising spend, revenue, conversions, impressions, clicks, and ROAS.
- **Channel Analysis:** Compare Facebook, Instagram, Google Ads, and YouTube performance.
- **Campaign Analysis:** Evaluate individual campaign effectiveness.
- **Audience Segmentation:** Identify high-performing customer segments.
- **Budget Optimization:** Compare platform-level advertising efficiency and generate preliminary recommendations.
- **Automated Marketing Insights:** Generate performance-based observations.
- **Report Export:** Download campaign data in CSV and multi-sheet Excel formats.
- **Interactive Filters:** Filter results by advertising platform, campaign objective, and date range.
- **Data Validation:** Check for missing columns, invalid dates, duplicate records, and inconsistent values.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Core programming |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical calculations |
| Streamlit | Interactive dashboard |
| Plotly | Data visualization |
| OpenPyXL | Excel report generation |

## Marketing Metrics

- **CTR:** Clicks / Impressions × 100
- **CPC:** Advertising Spend / Clicks
- **Conversion Rate:** Conversions / Clicks × 100
- **CPA:** Advertising Spend / Conversions
- **ROAS:** Revenue / Advertising Spend

## Dataset

The project uses 400 simulated marketing campaign records generated with Python.

**Advertising platforms:** Facebook, Instagram, Google Ads, YouTube.

**Audience segments:** Students, Young Professionals, Families, Online Shoppers.

**Campaign objectives:** Sales, Awareness, Traffic, Retargeting.

All data is fictional and intended for educational and portfolio demonstration purposes. It does not represent actual company or advertising-platform performance.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/marketing-campaign-performance-analyzer.git
```

### 2. Navigate to the project folder

```bash
cd marketing-campaign-performance-analyzer
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the dashboard

```bash
python -m streamlit run app.py
```

The dashboard will open at:

`http://localhost:8501`

## Project Structure

```text
marketing-campaign-performance-analyzer/
│
├── data/
│   └── campaigns.csv
│
├── app.py
├── create_dataset.py
├── analyze_data.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Business Applications

This project demonstrates how marketing analytics can help businesses:

- Evaluate digital advertising channel efficiency.
- Identify customer segments with stronger performance.
- Monitor campaign-level KPIs.
- Compare advertising expenditure against generated revenue.
- Develop preliminary budget allocation recommendations.
- Convert raw marketing data into actionable insights.

## Limitations

- The dataset is simulated, not collected from actual advertising platforms.
- ROAS does not account for product costs, operating expenses, or profit margins.
- Budget recommendations are preliminary and require further validation before real-world implementation.

## Author

**Saimon Sakib Shoishob**

Business Graduate | Management Information Systems

Dhaka, Bangladesh

[LinkedIn](https://www.linkedin.com/in/saimon-sakib-shoishob-884378282/)

---

*Built as a practical portfolio project to demonstrate Python-based marketing analytics, business intelligence, and data-driven decision-making.*

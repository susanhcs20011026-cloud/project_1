# Digital Marketing Conversion Dashboard

An interactive Streamlit dashboard that explores what drives customer conversion in digital marketing campaigns through engagement analysis, channel performance evaluation, statistical testing, and customer segmentation.

# Project Overview

This project analyzes a digital marketing campaign dataset to identify the factors that most strongly influence customer conversion behavior.

The dashboard combines interactive visualizations, business performance metrics, statistical testing, and machine learning segmentation to move beyond descriptive analytics toward actionable marketing insights.

The final dashboard includes:

* Interactive filtering and drill-down analysis
* Statistical significance testing (Chi-square)
* ROAS and CAC marketing efficiency analysis
* K-Means customer segmentation
* Funnel analysis and engagement tracking
* Dynamic narrative insights that update based on selected filters

# Dataset

**Source:** Kaggle — Predict Conversion in Digital Marketing Dataset

**Dataset Size:**

* 8,000 customers
* 20+ features

### Key Variables

#### Demographics

* Age
* Gender
* Income

#### Campaign Attributes

* CampaignChannel
* CampaignType
* AdSpend

#### Engagement Metrics

* TimeOnSite
* PagesPerVisit
* EmailOpens
* EmailClicks

#### Target Variable

* Conversion

  * 1 = Converted
  * 0 = Not Converted


# Research Questions

This dashboard explores several key marketing analytics questions:

1. Does deeper engagement lead to higher conversion rates?

2. Which marketing channels perform best in terms of:

   * conversion rate
   * ROAS (Return on Ad Spend)
   * CAC (Customer Acquisition Cost)

3. Are performance differences statistically significant?

4. Where do users drop off in the customer funnel before converting?

5. Are there distinct customer behavior segments within the audience?

# Dashboard Features

## Interactive Controls

The sidebar allows users to dynamically filter the dashboard by:

* Campaign channel
* Campaign type
* Gender
* Age range

All charts and findings update in real time.


## Visualizations

### 1. Engagement vs Conversion

Interactive line chart showing how engagement metrics relate to conversion rate.

### 2. Channel Drill-Down Analysis

Interactive channel comparison with demographic and campaign-type breakdowns.

### 3. A/B Statistical Testing

Chi-square testing used to determine whether conversion differences are statistically significant.

### 4. ROAS & CAC Analysis

Business efficiency analysis comparing:

* Return on Ad Spend
* Customer Acquisition Cost
* Revenue efficiency by channel

### 5. Customer Segmentation (K-Means)

Machine learning clustering used to identify:

* High-value users
* Mid-active users
* At-risk users

### 6. Funnel Analysis

Visualization of customer drop-off across:

* Email opens
* Email clicks
* Final conversion

# Technologies Used

* Streamlit
* Pandas
* NumPy
* Plotly
* SciPy
* Scikit-learn

# Setup Instructions

## 1. Clone or Download the Repository

```bash
git clone <repository-link>
```

## 2. Create and Activate a Virtual Environment

### Mac / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the Dashboard

```bash
streamlit run app.py
```

## 5. Open in Browser

Streamlit will automatically open:

```text
http://localhost:8501
```

# Key Findings

Several major patterns emerged from the analysis:

* User engagement is strongly associated with conversion behavior.
* Marketing channel performance varies significantly.
* Certain channels achieve substantially higher ROAS and lower CAC.
* The largest customer drop-off occurs between email open and click stages.
* K-Means clustering reveals distinct customer archetypes with very different conversion behaviors.

# Future Improvements

Given additional time and resources, future extensions could include:

* Predictive machine learning models
* Time-series campaign analysis
* Real-time dashboard deployment
* Personalized recommendation systems
* Advanced attribution modeling
* A/B experimentation framework

# Collaboration Statement

This project was completed independently with the assistance of AI tools including ChatGPT and Claude.

AI tools were used to assist with:

* debugging Streamlit and Plotly code
* refining dashboard styling and layout
* brainstorming visualization ideas
* improving narrative explanations
* organizing project structure

All final coding decisions, analytical interpretations, visualization selections, and project organization were reviewed and finalized independently by the author.


# Author

Susan Huang
Data Visualization Final Project

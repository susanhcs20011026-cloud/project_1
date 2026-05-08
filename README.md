Digital Marketing Conversion Dashboard
A Streamlit dashboard that explores what drives customer conversion in digital marketing campaigns.

Project Structure
project_1/
├── app.py
├── digital_marketing_campaign_dataset_2.csv
├── requirements.txt
└── README.md

Dataset

Source: Kaggle — Predict Conversion in Digital Marketing Dataset
Size: 8,000 customers, 20 features
Key columns:

Age, Gender, Income — demographic information
CampaignChannel, CampaignType, AdSpend — campaign attributes
TimeOnSite, PagesPerVisit, EmailOpens, EmailClicks — engagement metrics
Conversion — binary target variable (1 = converted, 0 = not converted)


Research Question
What factors most strongly predict whether a customer converts?
The dashboard examines three angles:

Does higher engagement (time on site) lead to higher conversion rates?
Which marketing channel delivers the best ROI?
Where do users drop off in the email funnel before converting?


Setup Instructions
1. Clone or download the project folder
2. Create and activate a virtual environment
bashpython -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate.bat       # Windows
3. Install dependencies
bashpip install -r requirements.txt
4. Run the dashboard
bashstreamlit run app.py
5. Open in browser
Streamlit will automatically open http://localhost:8501

Features

Sidebar filters — filter by campaign channel, campaign type, gender, and age range; all charts update in real time
Toggle switch — switch the first chart between Time on Site and Email Clicks
3 interactive visualizations built with Plotly:

Line chart: Time on Site vs Conversion Rate
Bar chart: ROI by Campaign Channel
Funnel chart: Customer drop-off across email stages


Key metrics — conversion rate, avg time on site, avg ad spend, avg email clicks
Raw data table — view filtered data directly in the dashboard


Requirements
streamlit
pandas
plotly

Author
Data Visualization Final Project

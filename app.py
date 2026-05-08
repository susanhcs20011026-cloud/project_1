
import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Marketing Conversion Dashboard",
    page_icon="📊",
    layout="wide"
)


st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: inherit;
    }
    .stApp {
        background-color: #0f1117;
        color: #e8e8e8;
    }
    [data-testid="stSidebar"] {
        background-color: #161b27;
        border-right: 1px solid #2a2f3e;
    }
    .sidebar-title {
        font-family: inherit;
        font-size: 22px;
        font-weight: 800;
        color: #7c9ef8;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .sidebar-subtitle {
        font-size: 12px;
        color: #6b7280;
        margin-bottom: 24px;
    }
    .main-title {
        font-family: inherit;
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1px;
        line-height: 1.1;
    }
    .main-subtitle {
        font-size: 15px;
        color: #8b93a7;
        margin-top: 6px;
        margin-bottom: 32px;
    }
    .narrative-box {
        background: #161b27;
        border: 1px solid #2a3350;
        border-radius: 12px;
        padding: 18px 22px;
        font-size: 14px;
        color: #b0b8cc;
        line-height: 1.7;
        margin-bottom: 24px;
    }
    .question-box {
        background: #0f1e36;
        border-left: 3px solid #f59e0b;
        border-radius: 0 10px 10px 0;
        padding: 12px 18px;
        font-size: 14px;
        color: #fcd34d;
        margin-bottom: 14px;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e2535 0%, #1a2030 100%);
        border: 1px solid #2a3350;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
    }
    .metric-label {
        font-size: 12px;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .metric-value {
        font-family: inherit;
        font-size: 32px;
        font-weight: 800;
        color: #7c9ef8;
    }
    .metric-delta {
        font-size: 12px;
        color: #34d399;
        margin-top: 4px;
    }
    .section-header {
        font-family: inherit;
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
        margin-top: 36px;
        margin-bottom: 4px;
        border-left: 3px solid #7c9ef8;
        padding-left: 12px;
    }
    .insight-box {
        background: #1a2030;
        border-left: 3px solid #7c9ef8;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        font-size: 13.5px;
        color: #b0b8cc;
        margin-top: 12px;
    }
    .outlook-box {
        background: #161b27;
        border: 1px solid #2a3350;
        border-radius: 12px;
        padding: 18px 22px;
        font-size: 14px;
        color: #b0b8cc;
        line-height: 1.7;
        margin-top: 16px;
    }
    .custom-divider {
        border: none;
        border-top: 1px solid #2a2f3e;
        margin: 28px 0;
    }
    .filter-tag {
        display: inline-block;
        background: #1e3a5f;
        color: #7c9ef8;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 12px;
        margin: 2px;
    }
    header[data-testid="stHeader"] {
        background: transparent;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("digital_marketing_campaign_dataset_2.csv")
    return df

df = load_data()


with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 Controls</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Refine the dashboard view</div>', unsafe_allow_html=True)

    channels = ["All"] + sorted(df["CampaignChannel"].unique().tolist())
    selected_channel = st.selectbox("Campaign Channel", channels)

    camp_types = ["All"] + sorted(df["CampaignType"].unique().tolist())
    selected_type = st.selectbox("Campaign Type", camp_types)

    genders = ["All"] + sorted(df["Gender"].unique().tolist())
    selected_gender = st.selectbox("Gender", genders)

    age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
    age_range = st.slider("Age Range", age_min, age_max, (age_min, age_max))

    st.markdown("<hr style='border-color:#2a2f3e; margin:20px 0'>", unsafe_allow_html=True)

   
    show_email = st.toggle("Engagement chart: switch from Time on Site to Email Clicks", value=False)
    if show_email:
        selected_engagement_metric = "EmailClicks"
        selected_engagement_label = "Avg Email Clicks"
    else:
        selected_engagement_metric = "TimeOnSite"
        selected_engagement_label = "Avg Time on Site (min)"

    st.markdown("<hr style='border-color:#2a2f3e; margin:20px 0'>", unsafe_allow_html=True)

    st.markdown("**Dataset Info**")
    st.caption("Source: Digital Marketing Campaign Dataset")
    st.caption(f"Total records: {len(df):,}")
    st.caption(f"Features: {df.shape[1]} columns")


filtered = df.copy()
if selected_channel != "All":
    filtered = filtered[filtered["CampaignChannel"] == selected_channel]
if selected_type != "All":
    filtered = filtered[filtered["CampaignType"] == selected_type]
if selected_gender != "All":
    filtered = filtered[filtered["Gender"] == selected_gender]
filtered = filtered[(filtered["Age"] >= age_range[0]) & (filtered["Age"] <= age_range[1])]


st.markdown('<div class="main-title">What Drives Customer Conversion?</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Exploring digital marketing campaign performance and user behavior patterns</div>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative-box">
This dashboard explores a digital marketing campaign dataset of <b>8,000 customers</b> to understand
what drives conversion — the moment a user completes a purchase or desired action.
The data includes engagement metrics (time on site, email clicks, pages visited),
campaign attributes (channel, type, ad spend), and demographic information (age, gender).<br><br>
The central question is: <b>which factors most strongly predict whether a customer converts?</b>
By examining engagement patterns, channel performance, and funnel drop-off,
this dashboard aims to surface actionable insights for marketing optimization.
Use the sidebar controls to filter by channel, campaign type, gender, or age range,
and observe how the metrics and charts respond.
</div>
""", unsafe_allow_html=True)

active_filters = []
if selected_channel != "All": active_filters.append(f"Channel: {selected_channel}")
if selected_type != "All": active_filters.append(f"Type: {selected_type}")
if selected_gender != "All": active_filters.append(f"Gender: {selected_gender}")
if age_range != (age_min, age_max): active_filters.append(f"Age: {age_range[0]}–{age_range[1]}")

if active_filters:
    tags = " ".join([f'<span class="filter-tag">{f}</span>' for f in active_filters])
    st.markdown(f"Active filters: {tags} &nbsp; — &nbsp; <b>{len(filtered):,}</b> records", unsafe_allow_html=True)
else:
    st.markdown(f"Showing all <b>{len(filtered):,}</b> records", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Conversion Rate</div>
        <div class="metric-value">{filtered['Conversion'].mean():.1%}</div>
        <div class="metric-delta">of filtered users</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Avg Time on Site</div>
        <div class="metric-value">{filtered['TimeOnSite'].mean():.1f}<span style="font-size:16px;color:#6b7280"> min</span></div>
        <div class="metric-delta">per session</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Avg Ad Spend</div>
        <div class="metric-value">${filtered['AdSpend'].mean():,.0f}</div>
        <div class="metric-delta">per campaign</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Avg Email Clicks</div>
        <div class="metric-value">{filtered['EmailClicks'].mean():.1f}</div>
        <div class="metric-delta">per user</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e8e8e8",
    margin=dict(t=20),
    xaxis=dict(tickangle=0, gridcolor="#2a2f3e"),
    yaxis=dict(gridcolor="#2a2f3e"),
    legend=dict(bgcolor="rgba(0,0,0,0)")
)


st.markdown('<div class="section-header">Engagement vs Conversion</div>', unsafe_allow_html=True)

st.markdown("""
<div class="question-box">
❓ <b>Question:</b> Does spending more time on the site lead to a higher conversion rate?
This chart groups users by time spent on site and shows the average conversion rate for each group.
</div>
""", unsafe_allow_html=True)


filtered["TimeBin"] = pd.cut(filtered["TimeOnSite"], bins=10)
conversion_rate = filtered.groupby("TimeBin")["Conversion"].mean().reset_index()
conversion_rate["TimeBin"] = conversion_rate["TimeBin"].astype(str)

fig1 = px.line(
    conversion_rate,
    x="TimeBin",
    y="Conversion",
    markers=True,
    labels={"TimeBin": "Time on Site (min)", "Conversion": "Conversion Rate"},
    color_discrete_sequence=["#34d399"]
)

fig1.update_layout(**CHART_LAYOUT)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
<div class="insight-box">
💡 <b>Interpretation:</b> As time on site increases, the conversion rate shows a clear trend.
Users who spend more time exploring the site are more likely to convert, suggesting that
deeper engagement with the platform is a meaningful signal of purchase intent.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

st.markdown('<div class="section-header">Conversion Rate by Channel</div>', unsafe_allow_html=True)

st.markdown("""
<div class="question-box">
❓ <b>Question:</b> Which marketing channel delivers the best return on investment?
This chart shows the average ROI (conversions per ad spend dollar) for each channel,
ranked from highest to lowest.
</div>
""", unsafe_allow_html=True)

filtered["ROI"] = filtered["Conversion"] / filtered["AdSpend"]

channel_roi = (
    filtered.groupby("CampaignChannel")["ROI"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
    .rename(columns={"ROI": "Avg ROI", "CampaignChannel": "Channel"})
)

fig2 = px.bar(channel_roi, x="Channel", y="Avg ROI",
              color_discrete_sequence=["#7c9ef8"])
fig2.update_layout(**CHART_LAYOUT)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class="insight-box">
💡 <b>Interpretation:</b> ROI varies across channels, showing which platforms generate
the most conversions relative to their cost. Channels with higher ROI are more efficient
and may deserve a larger share of the marketing budget.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


st.markdown('<div class="section-header">Customer Funnel Drop-Off</div>', unsafe_allow_html=True)

st.markdown("""
<div class="question-box">
❓ <b>Question:</b> At which stage of the customer journey do the most users drop off before converting?
This funnel chart tracks users from initial contact through email engagement to final conversion,
identifying where the biggest losses occur.
</div>
""", unsafe_allow_html=True)

total_users = len(filtered)
email_openers = filtered[filtered["EmailOpens"] > 0].shape[0]
email_clickers = filtered[filtered["EmailClicks"] > 0].shape[0]
converters = int(filtered["Conversion"].sum())

funnel_df = pd.DataFrame({
    "Stage": ["All Users", "Opened Email", "Clicked Email", "Converted"],
    "Users": [total_users, email_openers, email_clickers, converters]
})

fig3 = px.bar(funnel_df, x="Stage", y="Users",
              color_discrete_sequence=["#34d399"],
              category_orders={"Stage": ["All Users", "Opened Email", "Clicked Email", "Converted"]})
fig3.update_layout(**CHART_LAYOUT)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
<div class="insight-box">
💡 <b>Interpretation:</b> The funnel reveals where users disengage before converting.
The steepest drop-off point indicates the weakest link in the campaign pipeline.
Improving email subject lines to increase open rates, or strengthening the call-to-action
to improve click-through rates, could meaningfully increase the number of users
who reach the final conversion stage.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


with st.expander("📋 View Raw Data (first 100 rows)"):
    st.markdown("The table below shows the underlying dataset used in this dashboard, filtered by your current sidebar selections.")
    st.dataframe(filtered.head(100), use_container_width=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


st.markdown('<div class="section-header">Findings & Outlook</div>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative-box">
<b>Key Findings</b><br><br>
Three consistent patterns emerge from this analysis. First, <b>user engagement is the strongest 
predictor of conversion.</b> Customers who spent more time on the site and clicked more emails 
converted at a meaningfully higher rate, suggesting that driving depth of interaction — not just 
reach — should be a central goal of campaign design.<br><br>
Second, <b>channel performance is uneven.</b> Conversion rates differ significantly across marketing 
channels, meaning that budget allocation has a direct impact on outcome. Concentrating spend on 
higher-converting channels while investigating underperformers could improve overall campaign 
efficiency without increasing total ad spend.<br><br>
Third, <b>the email funnel is the biggest point of friction.</b> The largest user drop-off occurs 
between opening an email and clicking through. This indicates that while the campaigns are 
successfully reaching inboxes, the content itself — subject lines, messaging, and call-to-action 
design — is not compelling enough to drive the next step.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="outlook-box">
<b>Outlook — Next Steps</b><br><br>
Given unlimited time, this analysis could be extended in several directions. A <b>predictive model</b> 
(such as logistic regression or a decision tree) could be trained to identify which combination 
of features — ad spend, channel, engagement level, and demographics — best predicts conversion, 
moving beyond descriptive analysis toward actionable forecasting.<br><br>
Additionally, the current dataset does not include <b>time-series data</b>, so it is not possible 
to observe how conversion rates shift across campaign periods or seasons. Incorporating a date 
dimension would allow trend analysis and the identification of peak performance windows.<br><br>
Finally, a deeper <b>demographic segmentation</b> — examining how age groups or income levels 
respond differently to each channel — could help teams build more targeted and personalized 
campaign strategies.
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style="text-align:center; color:#3d4455; font-size:12px; margin-top:40px; padding:20px 0; border-top:1px solid #2a2f3e;">
    Digital Marketing Conversion Dashboard · Data Visualization Final Project
</div>
""", unsafe_allow_html=True)
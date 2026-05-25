import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2_contingency
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="Marketing Conversion Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: inherit; }
    .stApp { background-color: #0f1117; color: #e8e8e8; }
    [data-testid="stSidebar"] { background-color: #161b27; border-right: 1px solid #2a2f3e; }
    .sidebar-title { font-size: 22px; font-weight: 800; color: #7c9ef8; letter-spacing: -0.5px; margin-bottom: 4px; }
    .sidebar-subtitle { font-size: 12px; color: #6b7280; margin-bottom: 24px; }
    .main-title { font-size: 36px; font-weight: 800; color: #ffffff; letter-spacing: -1px; line-height: 1.1; }
    .main-subtitle { font-size: 15px; color: #8b93a7; margin-top: 6px; margin-bottom: 32px; }
    .narrative-box { background: #161b27; border: 1px solid #2a3350; border-radius: 12px; padding: 18px 22px; font-size: 14px; color: #b0b8cc; line-height: 1.7; margin-bottom: 24px; }
    .question-box { background: #0f1e36; border-left: 3px solid #f59e0b; border-radius: 0 10px 10px 0; padding: 12px 18px; font-size: 14px; color: #fcd34d; margin-bottom: 14px; }
    .metric-card { background: linear-gradient(135deg, #1e2535 0%, #1a2030 100%); border: 1px solid #2a3350; border-radius: 16px; padding: 20px 24px; text-align: center; }
    .metric-label { font-size: 12px; font-weight: 500; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .metric-value { font-size: 32px; font-weight: 800; color: #7c9ef8; }
    .metric-delta { font-size: 12px; color: #34d399; margin-top: 4px; }
    .section-header { font-size: 20px; font-weight: 700; color: #ffffff; margin-top: 36px; margin-bottom: 4px; border-left: 3px solid #7c9ef8; padding-left: 12px; }
    .insight-box { background: #1a2030; border-left: 3px solid #7c9ef8; border-radius: 0 10px 10px 0; padding: 14px 18px; font-size: 13.5px; color: #b0b8cc; margin-top: 12px; }
    .outlook-box { background: #161b27; border: 1px solid #2a3350; border-radius: 12px; padding: 18px 22px; font-size: 14px; color: #b0b8cc; line-height: 1.7; margin-top: 16px; }
    .custom-divider { border: none; border-top: 1px solid #2a2f3e; margin: 28px 0; }
    .filter-tag { display: inline-block; background: #1e3a5f; color: #7c9ef8; border-radius: 20px; padding: 2px 10px; font-size: 12px; margin: 2px; }
    .sig-badge { display: inline-block; border-radius: 6px; padding: 2px 8px; font-size: 11px; font-weight: 600; margin-left: 6px; }
    .sig-yes { background: #0d3320; color: #34d399; border: 1px solid #34d399; }
    .sig-no  { background: #2a1f10; color: #d1a054; border: 1px solid #d1a054; }
    .drilldown-back { background: #1e2535; border: 1px solid #2a3350; border-radius: 8px; padding: 8px 16px; font-size: 13px; color: #7c9ef8; cursor: pointer; display: inline-block; margin-bottom: 16px; }
    .segment-card { border-radius: 12px; padding: 14px 18px; font-size: 13px; margin-bottom: 12px; }
    .stButton > button { color: #7c9ef8 !important; background: #1e2535 !important; border: 1px solid #2a3350 !important; border-radius: 8px !important; } .stButton > button:hover { background: #2a3350 !important; color: #ffffff !important; }
    header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("digital_marketing_campaign_dataset_2.csv")
    return df

@st.cache_data
def run_kmeans(df):
    features = ["TimeOnSite", "PagesPerVisit", "EmailClicks", "EmailOpens", "AdSpend", "Conversion"]
    X = df[features].copy().fillna(0)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = km.fit_predict(X_scaled)
    df = df.copy()
    df["Segment"] = labels

    # Name segments by conversion rate
    seg_conv = df.groupby("Segment")["Conversion"].mean()
    order = seg_conv.sort_values(ascending=False).index.tolist()
    label_map = {order[0]: "High-value", order[1]: "Mid-active", order[2]: "At-risk"}
    df["Segment"] = df["Segment"].map(label_map)
    return df

df = load_data()
df_seg = run_kmeans(df)

if "drilldown_channel" not in st.session_state:
    st.session_state.drilldown_channel = None


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

    show_email = st.toggle("Switch engagement: Email Clicks vs Time on Site", value=False)
    selected_engagement_metric = "EmailClicks" if show_email else "TimeOnSite"
    selected_engagement_label = "Avg Email Clicks" if show_email else "Avg Time on Site (min)"

    st.markdown("<hr style='border-color:#2a2f3e; margin:20px 0'>", unsafe_allow_html=True)
    st.markdown("**Dataset Info**")
    st.caption("Source: Digital Marketing Campaign Dataset")
    st.caption(f"Total records: {len(df):,}")
    st.caption(f"Features: {df.shape[1]} columns")


filtered = df_seg.copy()
if selected_channel != "All":
    filtered = filtered[filtered["CampaignChannel"] == selected_channel]
if selected_type != "All":
    filtered = filtered[filtered["CampaignType"] == selected_type]
if selected_gender != "All":
    filtered = filtered[filtered["Gender"] == selected_gender]
filtered = filtered[(filtered["Age"] >= age_range[0]) & (filtered["Age"] <= age_range[1])]


CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e8e8e8",
    margin=dict(t=20),
    xaxis=dict(gridcolor="#2a2f3e"),
    yaxis=dict(gridcolor="#2a2f3e"),
    legend=dict(bgcolor="rgba(0,0,0,0)")
)


st.markdown('<div class="main-title">What Drives Customer Conversion?</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Exploring digital marketing campaign performance and user behavior patterns</div>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative-box">
<b>Data Source & Visualization Design</b><br><br>
This project uses the <a href="https://www.kaggle.com/datasets/rabieelkharoua/predict-conversion-in-digital-marketing-dataset/data" target="_blank" style="color:#7c9ef8;">
“Predict Conversion in Digital Marketing Dataset” </a> from Kaggle,
containing approximately 8,000 customer observations and engagement metrics.
            
The dashboard combines several visualization types to answer different analytical questions:
            
• Line charts were used to examine the relationship between engagement and conversion trends.
            
• Funnel analysis was used to identify customer drop-off points during the email conversion journey.
            
• Statistical testing (Chi-square) was applied to evaluate whether channel performance differences were statistically significant.
            
• ROAS and CAC visualizations were included to evaluate marketing efficiency and budget allocation strategy.
            
• K-Means clustering was used to identify distinct customer behavior segments and support audience targeting analysis.
</div>
""", unsafe_allow_html=True)

active_filters = []
if selected_channel != "All": active_filters.append(f"Channel: {selected_channel}")
if selected_type != "All": active_filters.append(f"Type: {selected_type}")
if selected_gender != "All": active_filters.append(f"Gender: {selected_gender}")
if age_range != (age_min, age_max): active_filters.append(f"Age: {age_range[0]}–{age_range[1]}")

if active_filters:
    tags = " ".join([f'<span class="filter-tag">{f}</span>' for f in active_filters])
    st.markdown(f"Active filters: {tags} &nbsp;—&nbsp; <b>{len(filtered):,}</b> records", unsafe_allow_html=True)
else:
    st.markdown(f"Showing all <b>{len(filtered):,}</b> records", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


st.markdown('<div class="section-header">Key Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Conversion Rate</div>
    <div class="metric-value">{filtered['Conversion'].mean():.1%}</div><div class="metric-delta">of filtered users</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Avg Time on Site</div>
    <div class="metric-value">{filtered['TimeOnSite'].mean():.1f}<span style="font-size:16px;color:#6b7280"> min</span></div><div class="metric-delta">per session</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Avg Ad Spend</div>
    <div class="metric-value">${filtered['AdSpend'].mean():,.0f}</div><div class="metric-delta">per campaign</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Avg Email Clicks</div>
    <div class="metric-value">{filtered['EmailClicks'].mean():.1f}</div><div class="metric-delta">per user</div></div>""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


st.markdown('<div class="section-header">Engagement vs Conversion</div>', unsafe_allow_html=True)
st.markdown("""<div class="question-box">❓ <b>Question:</b> Does spending more time on the site — or clicking more emails — lead to higher conversion?</div>""", unsafe_allow_html=True)

filtered["TimeBin"] = pd.cut(filtered["TimeOnSite"], bins=10)
conversion_rate = filtered.groupby("TimeBin")["Conversion"].mean().reset_index()
conversion_rate["TimeBin"] = conversion_rate["TimeBin"].astype(str)

fig1 = px.line(conversion_rate, x="TimeBin", y="Conversion", markers=True,
               labels={"TimeBin": "Time on Site (min)", "Conversion": "Conversion Rate"},
               color_discrete_sequence=["#34d399"])
fig1.update_layout(**CHART_LAYOUT)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""<div class="insight-box">💡 <b>Interpretation:</b> Users who spend more time exploring the site convert at a higher rate, confirming that deeper engagement is a meaningful signal of purchase intent.</div>""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# NEW 1 — CHANNEL DRILL-DOWN
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-header">Channel Performance — Click to Drill Down</div>', unsafe_allow_html=True)
st.markdown("""<div class="question-box">❓ <b>Question:</b> Which channel converts best? Click any bar to explore conversion breakdown by age group and gender within that channel.</div>""", unsafe_allow_html=True)

if st.session_state.drilldown_channel:
    channel = st.session_state.drilldown_channel
    if st.button(f"← Back to all channels"):
        st.session_state.drilldown_channel = None
        st.rerun()

    st.markdown(f"<div style='font-size:18px;font-weight:700;color:#7c9ef8;margin-bottom:16px;'>Deep dive: {channel}</div>", unsafe_allow_html=True)

    ch_data = filtered[filtered["CampaignChannel"] == channel]

    col_a, col_b = st.columns(2)
    with col_a:
        ch_data["AgeBin"] = pd.cut(ch_data["Age"], bins=[18, 28, 38, 48, 58, 70], labels=["18-28", "29-38", "39-48", "49-58", "59-70"])
        age_conv = ch_data.groupby("AgeBin", observed=True)["Conversion"].mean().reset_index()
        fig_age = px.bar(age_conv, x="AgeBin", y="Conversion",
                         title="Conversion rate by age group",
                         labels={"AgeBin": "Age group", "Conversion": "Conversion rate"},
                         color_discrete_sequence=["#7c9ef8"])
        fig_age.update_layout(**CHART_LAYOUT, title_font_color="#ffffff", title_font_size=14)
        st.plotly_chart(fig_age, use_container_width=True)

    with col_b:
        gender_conv = ch_data.groupby("Gender")["Conversion"].mean().reset_index()
        fig_gen = px.bar(gender_conv, x="Gender", y="Conversion",
                         title="Conversion rate by gender",
                         labels={"Gender": "Gender", "Conversion": "Conversion rate"},
                         color_discrete_sequence=["#f472b6", "#34d399", "#a78bfa"])
        fig_gen.update_layout(**CHART_LAYOUT, title_font_color="#ffffff", title_font_size=14)
        st.plotly_chart(fig_gen, use_container_width=True)

    type_conv = ch_data.groupby("CampaignType")["Conversion"].mean().reset_index()
    fig_type = px.bar(type_conv, x="CampaignType", y="Conversion",
                      title="Conversion rate by campaign type within this channel",
                      labels={"CampaignType": "Campaign type", "Conversion": "Conversion rate"},
                      color_discrete_sequence=["#f59e0b"])
    fig_type.update_layout(**CHART_LAYOUT, title_font_color="#ffffff", title_font_size=14)
    st.plotly_chart(fig_type, use_container_width=True)

    st.markdown(f"""<div class="insight-box">💡 <b>{channel} snapshot:</b> {len(ch_data):,} users · Conversion rate: {ch_data['Conversion'].mean():.1%} · Avg ad spend: ${ch_data['AdSpend'].mean():,.0f}</div>""", unsafe_allow_html=True)

else:
    channel_conv = filtered.groupby("CampaignChannel")["Conversion"].mean().sort_values(ascending=False).reset_index()
    channel_conv.columns = ["Channel", "Conversion Rate"]

    fig2 = px.bar(channel_conv, x="Channel", y="Conversion Rate",
                  color_discrete_sequence=["#7c9ef8"])
    fig2.update_layout(**CHART_LAYOUT)
    fig2.update_traces(customdata=channel_conv["Channel"])

    st.plotly_chart(fig2, use_container_width=True, key="channel_chart")

    st.markdown("""<div class="insight-box">💡 Click a bar above — or select a channel below — to enter drill-down view with age, gender, and campaign type breakdowns.</div>""", unsafe_allow_html=True)

    btn_cols = st.columns(len(channel_conv))
    for i, row in channel_conv.iterrows():
        with btn_cols[i]:
            if st.button(f"🔍 {row['Channel']}", use_container_width=True):
                st.session_state.drilldown_channel = row['Channel']
                st.rerun()

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# NEW 2 — A/B SIGNIFICANCE TESTING
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-header">A/B Significance Testing</div>', unsafe_allow_html=True)
st.markdown("""<div class="question-box">❓ <b>Question:</b> Are the conversion rate differences between channels and campaign types statistically significant, or could they be due to random chance? (Chi-square test, α = 0.05)</div>""", unsafe_allow_html=True)

ab_col1, ab_col2 = st.columns(2)

with ab_col1:
    st.markdown("<div style='font-size:14px;font-weight:600;color:#e8e8e8;margin-bottom:10px;'>Channel vs Conversion</div>", unsafe_allow_html=True)
    ch_ct = pd.crosstab(filtered["CampaignChannel"], filtered["Conversion"])
    chi2_ch, p_ch, _, _ = chi2_contingency(ch_ct)

    ch_rates = filtered.groupby("CampaignChannel")["Conversion"].agg(["mean", "count"]).reset_index()
    ch_rates.columns = ["Channel", "Conv. Rate", "N"]
    ch_rates["Conv. Rate"] = (ch_rates["Conv. Rate"] * 100).round(2)

    sig_label_ch = f'<span class="sig-badge sig-yes">✓ Significant (p={p_ch:.4f})</span>' if p_ch < 0.05 else f'<span class="sig-badge sig-no">✗ Not significant (p={p_ch:.4f})</span>'
    st.markdown(f"Chi-square statistic: **{chi2_ch:.2f}** {sig_label_ch}", unsafe_allow_html=True)

    fig_ab1 = px.bar(ch_rates, x="Channel", y="Conv. Rate",
                     color_discrete_sequence=["#7c9ef8"],
                     labels={"Conv. Rate": "Conversion rate (%)"})
    fig_ab1.add_hline(y=filtered["Conversion"].mean()*100,
                      line_dash="dot", line_color="#f59e0b",
                      annotation_text="Overall avg", annotation_font_color="#f59e0b")
    fig_ab1.update_layout(**{**CHART_LAYOUT, "margin": dict(t=30)})
    st.plotly_chart(fig_ab1, use_container_width=True)

with ab_col2:
    st.markdown("<div style='font-size:14px;font-weight:600;color:#e8e8e8;margin-bottom:10px;'>Campaign Type vs Conversion</div>", unsafe_allow_html=True)
    ct_ct = pd.crosstab(filtered["CampaignType"], filtered["Conversion"])
    chi2_ct, p_ct, _, _ = chi2_contingency(ct_ct)

    ct_rates = filtered.groupby("CampaignType")["Conversion"].agg(["mean", "count"]).reset_index()
    ct_rates.columns = ["Type", "Conv. Rate", "N"]
    ct_rates["Conv. Rate"] = (ct_rates["Conv. Rate"] * 100).round(2)

    sig_label_ct = f'<span class="sig-badge sig-yes">✓ Significant (p={p_ct:.4f})</span>' if p_ct < 0.05 else f'<span class="sig-badge sig-no">✗ Not significant (p={p_ct:.4f})</span>'
    st.markdown(f"Chi-square statistic: **{chi2_ct:.2f}** {sig_label_ct}", unsafe_allow_html=True)

    fig_ab2 = px.bar(ct_rates, x="Type", y="Conv. Rate",
                     color_discrete_sequence=["#34d399"],
                     labels={"Conv. Rate": "Conversion rate (%)"})
    fig_ab2.add_hline(y=filtered["Conversion"].mean()*100,
                      line_dash="dot", line_color="#f59e0b",
                      annotation_text="Overall avg", annotation_font_color="#f59e0b")
    fig_ab2.update_layout(**{**CHART_LAYOUT, "margin": dict(t=30)})
    st.plotly_chart(fig_ab2, use_container_width=True)

st.markdown("""<div class="insight-box">💡 <b>Interpretation:</b> The dashed amber line marks the overall conversion average — bars above it outperform the baseline. A green <b>✓ Significant</b> badge confirms the difference is unlikely to be random chance, making it safe to reallocate budget based on these results.</div>""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# NEW 3 — ROAS / CAC ANALYSIS
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-header">ROAS & CAC Analysis</div>', unsafe_allow_html=True)
st.markdown("""<div class="question-box">❓ <b>Question:</b> Beyond raw conversion rate — which channels deliver the most revenue-efficient outcomes? ROAS measures revenue returned per ad dollar; CAC measures the cost to acquire one converting customer.</div>""", unsafe_allow_html=True)

REVENUE_PER_CONVERSION = st.slider("Assumed revenue per conversion ($)", 50, 500, 150, step=10)

roas_df = filtered.groupby("CampaignChannel").agg(
    total_spend=("AdSpend", "sum"),
    conversions=("Conversion", "sum"),
    users=("Conversion", "count")
).reset_index()

roas_df["ROAS"] = (roas_df["conversions"] * REVENUE_PER_CONVERSION) / roas_df["total_spend"]
roas_df["CAC"] = roas_df["total_spend"] / roas_df["conversions"].replace(0, np.nan)
roas_df = roas_df.sort_values("ROAS", ascending=False)

benchmark_roas = roas_df["ROAS"].median()
benchmark_cac  = roas_df["CAC"].median()

roas_col1, roas_col2 = st.columns(2)

with roas_col1:
    fig_roas = px.bar(roas_df, x="CampaignChannel", y="ROAS",
                      color="ROAS",
                      color_continuous_scale=["#1e2535", "#3b5998", "#7c9ef8", "#34d399"],
                      labels={"CampaignChannel": "Channel", "ROAS": "ROAS (×)"})
    fig_roas.add_hline(y=benchmark_roas, line_dash="dot", line_color="#f59e0b",
                       annotation_text=f"Median ROAS {benchmark_roas:.2f}×",
                       annotation_font_color="#f59e0b")
    fig_roas.update_layout(**{**CHART_LAYOUT, "margin": dict(t=40)}, coloraxis_showscale=False,
                           title="Return on Ad Spend by channel", title_font_color="#ffffff", title_font_size=14)
    st.plotly_chart(fig_roas, use_container_width=True)

with roas_col2:
    fig_cac = px.bar(roas_df.sort_values("CAC"), x="CampaignChannel", y="CAC",
                     color="CAC",
                     color_continuous_scale=["#34d399", "#7c9ef8", "#3b5998", "#1e2535"],
                     labels={"CampaignChannel": "Channel", "CAC": "CAC ($)"})
    fig_cac.add_hline(y=benchmark_cac, line_dash="dot", line_color="#f59e0b",
                      annotation_text=f"Median CAC ${benchmark_cac:,.0f}",
                      annotation_font_color="#f59e0b")
    fig_cac.update_layout(**{**CHART_LAYOUT, "margin": dict(t=40)}, coloraxis_showscale=False,
                          title="Customer Acquisition Cost by channel", title_font_color="#ffffff", title_font_size=14)
    st.plotly_chart(fig_cac, use_container_width=True)

# ROAS vs CAC scatter
fig_scatter = px.scatter(roas_df, x="CAC", y="ROAS", text="CampaignChannel",
                         size="conversions", color="ROAS",
                         color_continuous_scale=["#1e2535", "#7c9ef8", "#34d399"],
                         labels={"CAC": "CAC ($) — lower is better", "ROAS": "ROAS (×) — higher is better"})
fig_scatter.update_traces(textposition="top center", textfont_color="#e8e8e8", textfont_size=11)
fig_scatter.add_vline(x=benchmark_cac, line_dash="dot", line_color="#4b5563")
fig_scatter.add_hline(y=benchmark_roas, line_dash="dot", line_color="#4b5563")
fig_scatter.add_annotation(x=roas_df["CAC"].min(), y=roas_df["ROAS"].max(),
                            text="★ Best quadrant", showarrow=False,
                            font=dict(color="#34d399", size=11))
fig_scatter.update_layout(**{**CHART_LAYOUT, "margin": dict(t=40)}, coloraxis_showscale=False,
                           title="ROAS vs CAC quadrant view (bubble size = conversions)",
                           title_font_color="#ffffff", title_font_size=14)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("""<div class="insight-box">💡 <b>Interpretation:</b> The quadrant view separates channels into four strategic buckets. Top-left (high ROAS, low CAC) is the ideal zone — channels here deserve more budget. Adjust the revenue-per-conversion slider above to reflect your actual product economics.</div>""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# NEW 4 — K-MEANS CUSTOMER SEGMENTATION
# ══════════════════════════════════════════════════════
st.markdown('<div class="section-header">Customer Segmentation (K-Means)</div>', unsafe_allow_html=True)
st.markdown("""<div class="question-box">❓ <b>Question:</b> Are there distinct customer archetypes in our audience? K-Means clustering groups users by behavior (time on site, email engagement, ad spend, pages visited) into three segments: High-value, Mid-active, and At-risk.</div>""", unsafe_allow_html=True)

seg_colors = {"High-value": "#34d399", "Mid-active": "#7c9ef8", "At-risk": "#f87171"}
seg_icons  = {"High-value": "🟢", "Mid-active": "🔵", "At-risk": "🔴"}

seg_summary = filtered.groupby("Segment").agg(
    users=("Conversion", "count"),
    conv_rate=("Conversion", "mean"),
    avg_time=("TimeOnSite", "mean"),
    avg_email=("EmailClicks", "mean"),
    avg_spend=("AdSpend", "mean"),
).reset_index()

card_cols = st.columns(3)
for i, row in seg_summary.iterrows():
    seg = row["Segment"]
    color = seg_colors.get(seg, "#7c9ef8")
    icon  = seg_icons.get(seg, "⚪")
    with card_cols[i % 3]:
        st.markdown(f"""
        <div style="background:#161b27;border:1px solid {color}44;border-left:4px solid {color};border-radius:12px;padding:18px 20px;margin-bottom:12px;">
          <div style="font-size:16px;font-weight:700;color:{color};margin-bottom:10px;">{icon} {seg}</div>
          <div style="font-size:13px;color:#8b93a7;line-height:2;">
            Users: <b style="color:#e8e8e8">{row['users']:,}</b><br>
            Conv. rate: <b style="color:{color}">{row['conv_rate']:.1%}</b><br>
            Avg time on site: <b style="color:#e8e8e8">{row['avg_time']:.1f} min</b><br>
            Avg email clicks: <b style="color:#e8e8e8">{row['avg_email']:.1f}</b><br>
            Avg ad spend: <b style="color:#e8e8e8">${row['avg_spend']:,.0f}</b>
          </div>
        </div>""", unsafe_allow_html=True)

seg_col1, seg_col2 = st.columns(2)

with seg_col1:
    fig_seg_conv = px.bar(seg_summary, x="Segment", y="conv_rate",
                          color="Segment",
                          color_discrete_map=seg_colors,
                          labels={"conv_rate": "Conversion rate", "Segment": "Segment"},
                          title="Conversion rate by segment")
    fig_seg_conv.update_layout(**{**CHART_LAYOUT, "margin": dict(t=40)}, showlegend=False,
                                title_font_color="#ffffff", title_font_size=14)
    st.plotly_chart(fig_seg_conv, use_container_width=True)

with seg_col2:
    metrics = ["avg_time", "avg_email", "avg_spend"]
    metric_labels = {"avg_time": "Avg time on site", "avg_email": "Avg email clicks", "avg_spend": "Avg ad spend"}

    fig_radar = go.Figure()
    for _, row in seg_summary.iterrows():
        seg = row["Segment"]
        vals = [row[m] for m in metrics]
        max_vals = [seg_summary[m].max() for m in metrics]
        norm_vals = [v / mx if mx > 0 else 0 for v, mx in zip(vals, max_vals)]
        norm_vals += [norm_vals[0]]
        labels = [metric_labels[m] for m in metrics] + [metric_labels[metrics[0]]]
        fig_radar.add_trace(go.Scatterpolar(
            r=norm_vals, theta=labels, fill="toself",
            name=seg, line_color=seg_colors.get(seg, "#7c9ef8"),
            fillcolor="rgba(52,211,153,0.2)" if seg == "High-value" else ("rgba(124,158,248,0.2)" if seg == "Mid-active" else "rgba(248,113,113,0.2)"),
            opacity=0.7
        ))
    fig_radar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8e8e8",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], gridcolor="#2a2f3e", tickfont_color="#6b7280"),
            angularaxis=dict(gridcolor="#2a2f3e")
        ),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=40, b=20),
        title="Segment behavioral profile (normalized)",
        title_font_color="#ffffff", title_font_size=14
    )
    st.plotly_chart(fig_radar, use_container_width=True)

seg_channel = filtered.groupby(["Segment", "CampaignChannel"])["Conversion"].mean().reset_index()
fig_seg_ch = px.bar(seg_channel, x="CampaignChannel", y="Conversion", color="Segment",
                    barmode="group", color_discrete_map=seg_colors,
                    labels={"CampaignChannel": "Channel", "Conversion": "Conversion rate", "Segment": "Segment"},
                    title="Conversion rate per segment × channel")
fig_seg_ch.update_layout(**{**CHART_LAYOUT, "margin": dict(t=40)}, title_font_color="#ffffff", title_font_size=14)
st.plotly_chart(fig_seg_ch, use_container_width=True)

st.markdown("""<div class="insight-box">💡 <b>Interpretation:</b> The three segments reveal meaningfully different profiles. High-value users convert most frequently and engage deeply — retaining them is the top priority. At-risk users have low engagement across all signals; targeted re-engagement campaigns (higher-frequency email, personalised offers) may recover a portion before they churn. The segment × channel chart shows which channels over- or under-perform for each group.</div>""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)


st.markdown('<div class="section-header">Customer Funnel Drop-Off</div>', unsafe_allow_html=True)
st.markdown("""<div class="question-box">❓ <b>Question:</b> At which stage do most users disengage before converting?</div>""", unsafe_allow_html=True)

total_users = len(filtered)
email_openers  = filtered[filtered["EmailOpens"] > 0].shape[0]
email_clickers = filtered[filtered["EmailClicks"] > 0].shape[0]
converters     = int(filtered["Conversion"].sum())

funnel_df = pd.DataFrame({
    "Stage": ["All Users", "Opened Email", "Clicked Email", "Converted"],
    "Users": [total_users, email_openers, email_clickers, converters]
})
funnel_df["Drop %"] = (1 - funnel_df["Users"] / funnel_df["Users"].shift(1)).fillna(0)

fig3 = px.bar(funnel_df, x="Stage", y="Users",
              color_discrete_sequence=["#34d399"],
              category_orders={"Stage": ["All Users", "Opened Email", "Clicked Email", "Converted"]})
fig3.update_layout(**CHART_LAYOUT)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""<div class="insight-box">💡 <b>Interpretation:</b> The steepest drop-off marks the weakest link. Improving email subject lines to lift open rates, or strengthening calls-to-action to improve click-through, are the highest-leverage interventions.</div>""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

with st.expander("📋 View Raw Data (first 100 rows)"):
    st.markdown("Filtered dataset including K-Means segment assignment.")
    st.dataframe(filtered.head(100), use_container_width=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

st.markdown('<div class="section-header">Findings & Outlook</div>', unsafe_allow_html=True)

# Dynamic Findings Calculations
rev_per_conv = REVENUE_PER_CONVERSION

# 1. Engagement correlation
corr_time = filtered["TimeOnSite"].corr(filtered["Conversion"])
corr_email = filtered["EmailClicks"].corr(filtered["Conversion"])
stronger_engagement = "time on site" if abs(corr_time) >= abs(corr_email) else "email clicks"
stronger_corr = max(abs(corr_time), abs(corr_email))

# 2. Channel significance (recompute from filtered)
_ch_ct = pd.crosstab(filtered["CampaignChannel"], filtered["Conversion"])
_chi2_ch, _p_ch, _, _ = chi2_contingency(_ch_ct)
ch_sig_text = f"statistically significant (χ²={_chi2_ch:.2f}, p={_p_ch:.4f})" if _p_ch < 0.05 \
              else f"not statistically significant (χ²={_chi2_ch:.2f}, p={_p_ch:.4f})"
ch_sig_action = "making budget reallocation a data-safe decision" if _p_ch < 0.05 \
                else "suggesting channel mix may need broader re-evaluation rather than simple reallocation"

# 3. Top / bottom channel by conversion rate
_ch_conv = filtered.groupby("CampaignChannel")["Conversion"].mean().sort_values(ascending=False)
top_ch = _ch_conv.index[0]
top_ch_rate = _ch_conv.iloc[0]
bot_ch = _ch_conv.index[-1]
bot_ch_rate = _ch_conv.iloc[-1]

# 4. ROAS / CAC best channel
_roas_tmp = filtered.groupby("CampaignChannel").agg(
    total_spend=("AdSpend", "sum"),
    conversions=("Conversion", "sum")
).reset_index()
_roas_tmp["ROAS"] = (_roas_tmp["conversions"] * REVENUE_PER_CONVERSION) / _roas_tmp["total_spend"]
_roas_tmp["CAC"]  = _roas_tmp["total_spend"] / _roas_tmp["conversions"].replace(0, np.nan)
best_roas_ch  = _roas_tmp.loc[_roas_tmp["ROAS"].idxmax(), "CampaignChannel"]
best_roas_val = _roas_tmp["ROAS"].max()
best_cac_ch   = _roas_tmp.loc[_roas_tmp["CAC"].idxmin(), "CampaignChannel"]
best_cac_val  = _roas_tmp["CAC"].min()

# 5. Segmentation stats
_hv = filtered[filtered["Segment"] == "High-value"]
_ar = filtered[filtered["Segment"] == "At-risk"]
hv_conv  = _hv["Conversion"].mean() if len(_hv) > 0 else 0
ar_conv  = _ar["Conversion"].mean() if len(_ar) > 0 else 0
hv_count = len(_hv)
ar_count = len(_ar)
conv_gap = hv_conv - ar_conv

# 6. Funnel biggest drop
_stages = [total_users, email_openers, email_clickers, converters]
_labels = ["All Users → Opened Email", "Opened Email → Clicked Email", "Clicked Email → Converted"]
_drops  = [1 - _stages[i+1] / _stages[i] if _stages[i] > 0 else 0 for i in range(3)]
biggest_drop_label = _labels[int(np.argmax(_drops))]
biggest_drop_pct   = max(_drops)

# ── Render Dynamic Findings ─────────────────────────────────────────────────
st.markdown(f"""
<div class="narrative-box">
<b>Key Findings (dynamic data)<br>
This project explores customer conversion behavior in digital marketing campaigns through an interactive Streamlit dashboard combining engagement analysis, statistical testing, and customer segmentation.
The final dashboard combines engagement analysis, statistical testing, ROAS/CAC evaluation, customer segmentation, and dynamic narrative generation to support marketing decision-making and customer behavior analysis.</b><br>
<br><br>
<b>① Engagement drives conversion.</b>
Among the filtered <b>{len(filtered):,}</b> users,
<b>{stronger_engagement}</b> shows the strongest correlation with conversion
(r = {stronger_corr:.3f}).
Users with above-average time on site convert at
<b>{filtered[filtered["TimeOnSite"] > filtered["TimeOnSite"].median()]["Conversion"].mean():.1%}</b>
versus
<b>{filtered[filtered["TimeOnSite"] <= filtered["TimeOnSite"].median()]["Conversion"].mean():.1%}</b>
for those below the median — confirming that depth of engagement, not just reach, is the key lever.<br><br>

<b>② Channel performance differences are {ch_sig_text}</b>,
{ch_sig_action}.
The top-performing channel is <b>{top_ch}</b> ({top_ch_rate:.1%} conversion rate),
while <b>{bot_ch}</b> lags at {bot_ch_rate:.1%} —
a gap of <b>{(top_ch_rate - bot_ch_rate)*100:.1f} percentage points</b>.<br><br>

<b>③ ROAS and CAC point to {best_roas_ch} as the most efficient channel.</b>
At the assumed revenue of USD {rev_per_conv}/conversion,
<b>{best_roas_ch}</b> delivers a ROAS of <b>{best_roas_val:.2f}×</b>,
and <b>{best_cac_ch}</b> has the lowest customer acquisition cost at
<b>USD {best_cac_val:,.0f}</b> per converting user.<br><br>

<b>④ Segmentation reveals a {conv_gap*100:.1f} pp conversion gap</b> between archetypes.
The <b>High-value</b> segment ({hv_count:,} users) converts at <b>{hv_conv:.1%}</b>,
while the <b>At-risk</b> segment ({ar_count:,} users) converts at only <b>{ar_conv:.1%}</b>.
The biggest funnel drop-off occurs at the <b>{biggest_drop_label}</b> stage
({biggest_drop_pct:.1%} of users lost), identifying the highest-priority intervention point.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="outlook-box">
<b>Outlook — Next Steps</b><br><br>
Given these findings, three actions are most urgent.
First, invest in <b>deepening on-site engagement</b> — the {corr_time:.3f} correlation between time on site and conversion
suggests that UX improvements (better content, clearer navigation, stronger CTAs) could meaningfully lift revenue
without increasing ad spend.<br><br>
Second, <b>reallocate budget toward {best_roas_ch}</b> (ROAS {best_roas_val:.2f}×) and
<b>{best_cac_ch}</b> (CAC ${best_cac_val:,.0f}), and run controlled experiments
on lower-performing channels before cutting them entirely.<br><br>
Third, build a <b>segment-specific re-engagement campaign</b> targeting the {ar_count:,} At-risk users —
even recovering 10% of them to Mid-active status would add approximately
<b>{int(ar_count * 0.10 * (hv_conv - ar_conv)):,} incremental conversions</b>
based on current segment conversion rates.
<br><br>
If given additional time and resources, this project could be expanded using real-world marketing data from large companies such as Amazon or Target.  
Access to larger datasets would allow for more accurate analysis of customer engagement, conversion behavior, ROAS, CAC, and long-term customer retention patterns across different marketing channels.  
Future versions could include real-time campaign tracking, personalized recommendation systems based on customer segments, and automated A/B testing to support more advanced marketing decision-making and budget optimization.

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="outlook-box">
<b>Collaboration Statement</b><br><br>

This project was completed independently with the assistance of AI tools including ChatGPT and Claude.

AI tools were used to assist with:
- debugging Streamlit and Plotly code
- refining dashboard styling and layout
- organizing project structure
- One of the major improvements in the final version was the addition of dynamically generated findings and outlook sections. Instead of displaying static written summaries, the dashboard automatically recalculates correlations, conversion gaps, ROAS, CAC, funnel drop-off rates, and segmentation statistics based on the user’s selected filters.
Claude AI was used to assist in implementing portions of this dynamic narrative generation logic, including the integration of calculated metrics into Streamlit markdown components using Python f-strings. This transformed the dashboard from a static visualization project into a more interactive analytical storytelling system.
- The initial version of the dashboard focused primarily on three basic marketing visualizations: engagement vs conversion, channel ROI, and funnel analysis. With assistance from Claude AI for statistical analysis logic and advanced dashboard features, the final version expanded to include channel drill-down analysis, A/B significance testing, ROAS & CAC evaluation, K-Means customer segmentation, radar charts, and dynamic insight generation.
These additions transformed the project from a basic marketing dashboard into a more advanced analytical and statistical decision-support system focused on customer behavior, marketing efficiency, and segmentation insights.
- Initially, the dashboard used raw TimeOnSite values directly in the visualization. After reviewing the first chart, it became difficult to identify broader engagement trends because the data was too granular. Following GPT’s suggestion, the final version grouped users into pandas-generated intervals (pd.qcut) and calculated the average conversion rate for each group. This made the relationship between engagement and conversion behavior much clearer.
- K-Means clustering was a new concept and visualization approach that I learned with assistance from Claude AI during the development process. Claude helped explain how behavioral segmentation works and how clustering could be used to identify distinct customer groups based on engagement patterns.
All final coding decisions, analytical interpretations, and visualization selections were reviewed and finalized independently by the author.
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""<div style="text-align:center;color:#3d4455;font-size:12px;margin-top:40px;padding:20px 0;border-top:1px solid #2a2f3e;">
    Digital Marketing Conversion Dashboard · Data Visualization Final Project
</div>""", unsafe_allow_html=True)
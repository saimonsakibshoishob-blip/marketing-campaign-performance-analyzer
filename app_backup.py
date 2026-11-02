
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Marketing Campaign Analyzer",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    data = pd.read_csv("data/campaigns.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    return data

df = load_data()

# ==========================================
# 3. CALCULATE MARKETING METRICS
# ==========================================

def calculate_metrics(data):

    data = data.copy()

    data["CTR"] = np.where(
        data["Impressions"] > 0,
        data["Clicks"] / data["Impressions"] * 100,
        0
    )

    data["CPC_BDT"] = np.where(
        data["Clicks"] > 0,
        data["Spend_BDT"] / data["Clicks"],
        0
    )

    data["Conversion_Rate"] = np.where(
        data["Clicks"] > 0,
        data["Conversions"] / data["Clicks"] * 100,
        0
    )

    data["CPA_BDT"] = np.where(
        data["Conversions"] > 0,
        data["Spend_BDT"] / data["Conversions"],
        0
    )

    data["ROAS"] = np.where(
        data["Spend_BDT"] > 0,
        data["Revenue_BDT"] / data["Spend_BDT"],
        0
    )

    return data


df = calculate_metrics(df)

# ==========================================
# 4. DASHBOARD TITLE
# ==========================================

st.title("📊 Marketing Campaign Performance Analyzer")

st.caption(
    "A business intelligence dashboard for evaluating "
    "digital marketing performance."
)

st.info(
    "This portfolio project uses simulated marketing data. "
    "All financial figures are expressed in BDT."
)

# ==========================================
# 5. SIDEBAR FILTERS
# ==========================================

st.sidebar.title("Dashboard Filters")

platform_options = sorted(df["Platform"].unique())

selected_platforms = st.sidebar.multiselect(
    "Select Marketing Platforms",
    options=platform_options,
    default=platform_options
)

objective_options = sorted(df["Objective"].unique())

selected_objectives = st.sidebar.multiselect(
    "Select Campaign Objectives",
    options=objective_options,
    default=objective_options
)

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_df = df[
        (df["Platform"].isin(selected_platforms)) &
        (df["Objective"].isin(selected_objectives)) &
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date)
    ]

else:
    filtered_df = df.iloc[0:0]

# ==========================================
# 6. HANDLE EMPTY DATA
# ==========================================

if filtered_df.empty:

    st.warning(
        "No campaign data found for the selected filters. "
        "Please change your filters."
    )

    st.stop()

# ==========================================
# 7. EXECUTIVE OVERVIEW
# ==========================================

st.header("Executive Overview")

total_spend = filtered_df["Spend_BDT"].sum()
total_revenue = filtered_df["Revenue_BDT"].sum()
total_clicks = filtered_df["Clicks"].sum()
total_impressions = filtered_df["Impressions"].sum()
total_conversions = filtered_df["Conversions"].sum()

overall_ctr = (
    total_clicks / total_impressions * 100
    if total_impressions > 0 else 0
)

overall_cpa = (
    total_spend / total_conversions
    if total_conversions > 0 else 0
)

overall_roas = (
    total_revenue / total_spend
    if total_spend > 0 else 0
)

# KPI cards

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Ad Spend",
    f"৳{total_spend:,.0f}"
)

col2.metric(
    "Total Revenue",
    f"৳{total_revenue:,.0f}"
)

col3.metric(
    "Total Conversions",
    f"{total_conversions:,.0f}"
)

col4.metric(
    "ROAS",
    f"{overall_roas:.2f}x"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Total Impressions",
    f"{total_impressions:,.0f}"
)

col6.metric(
    "Total Clicks",
    f"{total_clicks:,.0f}"
)

col7.metric(
    "Click-Through Rate",
    f"{overall_ctr:.2f}%"
)

col8.metric(
    "Cost Per Acquisition",
    f"৳{overall_cpa:,.2f}"
)

st.divider()

# ==========================================
# 8. DASHBOARD TABS
# ==========================================

overview_tab, channel_tab, campaign_tab, insights_tab = st.tabs([
    "Executive Overview",
    "Channel Analysis",
    "Campaign Analysis",
    "Business Insights"
])

# ==========================================
# 9. EXECUTIVE OVERVIEW CHARTS
# ==========================================

with overview_tab:

    st.subheader("Revenue and Advertising Spend")

    chart_data = filtered_df.groupby("Platform", as_index=False).agg({
        "Revenue_BDT": "sum",
        "Spend_BDT": "sum"
    })

    chart_data = chart_data.melt(
        id_vars="Platform",
        value_vars=["Revenue_BDT", "Spend_BDT"],
        var_name="Metric",
        value_name="Amount"
    )

    fig = px.bar(
        chart_data,
        x="Platform",
        y="Amount",
        color="Metric",
        barmode="group",
        title="Revenue vs Advertising Spend by Platform",
        labels={
            "Amount": "Amount (BDT)",
            "Platform": "Marketing Platform"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Performance Trend")

    monthly_data = (
        filtered_df
        .set_index("Date")
        .resample("MS")
        .agg({
            "Spend_BDT": "sum",
            "Revenue_BDT": "sum"
        })
        .reset_index()
    )

    monthly_long = monthly_data.melt(
        id_vars="Date",
        value_vars=["Spend_BDT", "Revenue_BDT"],
        var_name="Metric",
        value_name="Amount"
    )

    trend_fig = px.line(
        monthly_long,
        x="Date",
        y="Amount",
        color="Metric",
        markers=True,
        title="Monthly Advertising Spend and Revenue"
    )

    st.plotly_chart(
        trend_fig,
        use_container_width=True
    )

# ==========================================
# 10. CHANNEL ANALYSIS
# ==========================================

with channel_tab:

    st.subheader("Marketing Channel Performance")

    channel_data = filtered_df.groupby(
        "Platform", as_index=False
    ).agg({
        "Impressions": "sum",
        "Clicks": "sum",
        "Spend_BDT": "sum",
        "Conversions": "sum",
        "Revenue_BDT": "sum"
    })

    channel_data["CTR"] = (
        channel_data["Clicks"] /
        channel_data["Impressions"] * 100
    )

    channel_data["CPC_BDT"] = (
        channel_data["Spend_BDT"] /
        channel_data["Clicks"].replace(0, np.nan)
    )

    channel_data["CPA_BDT"] = (
        channel_data["Spend_BDT"] /
        channel_data["Conversions"].replace(0, np.nan)
    )

    channel_data["ROAS"] = (
        channel_data["Revenue_BDT"] /
        channel_data["Spend_BDT"].replace(0, np.nan)
    )

    st.dataframe(
        channel_data.round(2),
        use_container_width=True,
        hide_index=True
    )

    roas_fig = px.bar(
        channel_data,
        x="Platform",
        y="ROAS",
        color="Platform",
        title="Return on Ad Spend by Platform"
    )

    st.plotly_chart(
        roas_fig,
        use_container_width=True
    )

    conversion_fig = px.bar(
        channel_data,
        x="Platform",
        y="Conversions",
        color="Platform",
        title="Conversions by Platform"
    )

    st.plotly_chart(
        conversion_fig,
        use_container_width=True
    )

# ==========================================
# 11. CAMPAIGN ANALYSIS
# ==========================================

with campaign_tab:

    st.subheader("Individual Campaign Performance")

    campaign_data = filtered_df.groupby(
        ["Campaign_ID", "Campaign_Name", "Platform", "Objective"],
        as_index=False
    ).agg({
        "Impressions": "sum",
        "Clicks": "sum",
        "Spend_BDT": "sum",
        "Conversions": "sum",
        "Revenue_BDT": "sum"
    })

    campaign_data["CTR"] = (
        campaign_data["Clicks"] /
        campaign_data["Impressions"].replace(0, np.nan) * 100
    )

    campaign_data["CPA_BDT"] = (
        campaign_data["Spend_BDT"] /
        campaign_data["Conversions"].replace(0, np.nan)
    )

    campaign_data["ROAS"] = (
        campaign_data["Revenue_BDT"] /
        campaign_data["Spend_BDT"].replace(0, np.nan)
    )

    st.dataframe(
        campaign_data.round(2),
        use_container_width=True,
        hide_index=True
    )

    top_campaigns = campaign_data.nlargest(5, "ROAS")

    top_fig = px.bar(
        top_campaigns,
        x="Campaign_Name",
        y="ROAS",
        color="Platform",
        title="Top 5 Campaigns by ROAS"
    )

    st.plotly_chart(
        top_fig,
        use_container_width=True
    )

# ==========================================
# 12. BUSINESS INSIGHTS
# ==========================================

with insights_tab:

    st.subheader("Automated Marketing Insights")

    if not channel_data.empty:

        best_roas = channel_data.loc[
            channel_data["ROAS"].idxmax()
        ]

        lowest_cpa = channel_data.loc[
            channel_data["CPA_BDT"].idxmin()
        ]

        highest_revenue = channel_data.loc[
            channel_data["Revenue_BDT"].idxmax()
        ]

        st.success(
            f"Highest ROAS: {best_roas['Platform']} "
            f"generated {best_roas['ROAS']:.2f}x ROAS."
        )

        st.info(
            f"Lowest acquisition cost: "
            f"{lowest_cpa['Platform']} had a CPA of "
            f"৳{lowest_cpa['CPA_BDT']:,.2f}."
        )

        st.info(
            f"Highest revenue: {highest_revenue['Platform']} "
            f"generated ৳{highest_revenue['Revenue_BDT']:,.2f}."
        )

        if overall_roas > 1:
            st.success(
                "Attributed revenue exceeds advertising spend. "
                "However, this does not establish profitability."
            )
        elif overall_roas == 1:
            st.warning(
                "Attributed revenue equals advertising spend. "
                "Other business costs are not covered."
            )
        else:
            st.warning(
                "Attributed revenue is below advertising spend. "
                "Review campaign efficiency and attribution."
            )

        st.subheader("Recommended Areas for Investigation")

        st.write(
            "1. Investigate whether high-ROAS campaigns can "
            "scale without losing efficiency."
        )

        st.write(
            "2. Review campaigns with high CPA and low conversion rates."
        )

        st.write(
            "3. Compare audience segments to identify "
            "opportunities for better targeting."
        )

        st.caption(
            "These are preliminary recommendations based on "
            "aggregated simulated data, not causal findings."
        )

# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.caption(
    "Marketing Campaign Performance Analyzer | "
    "Built with Python, Pandas, Streamlit and Plotly | "
    "Portfolio Project"
)

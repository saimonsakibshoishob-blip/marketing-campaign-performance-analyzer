
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from io import BytesIO
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import os

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

    file_path = "data/campaigns.csv"

    # Check whether the dataset exists
    if not os.path.exists(file_path):
        st.error("Dataset not found. Please check the data folder.")
        st.stop()

    # Load dataset
    df = pd.read_csv(file_path)

    # Required columns
    required_columns = [
        "Date",
        "Campaign_ID",
        "Campaign_Name",
        "Platform",
        "Objective",
        "Audience_Segment",
        "Impressions",
        "Clicks",
        "Spend_BDT",
        "Conversions",
        "Revenue_BDT"
    ]

    # Check missing columns
    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        st.error(f"Missing columns: {missing_columns}")
        st.stop()

    # Check empty dataset
    if df.empty:
        st.error("The dataset is empty.")
        st.stop()

    # Convert date column
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Remove records with invalid dates
    df = df.dropna(subset=["Date"])

    # Remove duplicate records
    df = df.drop_duplicates()

    # Validate numerical columns
    numeric_columns = [
        "Impressions",
        "Clicks",
        "Spend_BDT",
        "Conversions",
        "Revenue_BDT"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove rows with missing numerical values
    df = df.dropna(subset=numeric_columns)

    # Check impossible negative values
    for col in numeric_columns:
        df = df[df[col] >= 0]

    # Check logical consistency
    df = df[
        (df["Clicks"] <= df["Impressions"]) &
        (df["Conversions"] <= df["Clicks"])
    ]

    if df.empty:
        st.error("No valid records remain after data validation.")
        st.stop()

    return df

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

df = load_data()
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

overview_tab, channel_tab, campaign_tab, audience_tab, budget_tab, insights_tab = st.tabs([
    "Executive Overview",
    "Channel Analysis",
    "Campaign Analysis",
    "Audience Analysis",
    "Budget Optimization",
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
with audience_tab:
    st.subheader("Audience Segment Performance")

    audience_data = filtered_df.groupby(
        "Audience_Segment"
    ).agg(
        Impressions=("Impressions", "sum"),
        Clicks=("Clicks", "sum"),
        Spend_BDT=("Spend_BDT", "sum"),
        Conversions=("Conversions", "sum"),
        Revenue_BDT=("Revenue_BDT", "sum")
    ).reset_index()

    audience_data["CTR"] = (
        audience_data["Clicks"] /
        audience_data["Impressions"].replace(0, np.nan) * 100
    )

    audience_data["Conversion_Rate"] = (
        audience_data["Conversions"] /
        audience_data["Clicks"].replace(0, np.nan) * 100
    )

    audience_data["CPA_BDT"] = (
        audience_data["Spend_BDT"] /
        audience_data["Conversions"].replace(0, np.nan)
    )

    audience_data["ROAS"] = (
        audience_data["Revenue_BDT"] /
        audience_data["Spend_BDT"].replace(0, np.nan)
    )

    st.markdown("### Audience Performance")

    col1, col2, col3 = st.columns(3)

    best_revenue = audience_data.loc[
        audience_data["Revenue_BDT"].idxmax()
    ]

    best_conversion = audience_data.loc[
        audience_data["Conversion_Rate"].idxmax()
    ]

    best_roas = audience_data.loc[
        audience_data["ROAS"].idxmax()
    ]

    col1.metric(
        "Highest Revenue Segment",
        best_revenue["Audience_Segment"]
    )

    col2.metric(
        "Highest Conversion Rate",
        best_conversion["Audience_Segment"],
        f"{best_conversion['Conversion_Rate']:.2f}%"
    )

    col3.metric(
        "Highest ROAS Segment",
        best_roas["Audience_Segment"],
        f"{best_roas['ROAS']:.2f}x"
    )

    fig = px.bar(
        audience_data,
        x="Audience_Segment",
        y="Revenue_BDT",
        color="Audience_Segment",
        title="Revenue by Audience Segment"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        audience_data.round(2),
        use_container_width=True,
        hide_index=True
    )
    with budget_tab:
        st.subheader("Marketing Budget Optimization")

        # Calculate platform-level performance
        platform_budget = filtered_df.groupby("Platform").agg(
            Spend_BDT=("Spend_BDT", "sum"),
            Revenue_BDT=("Revenue_BDT", "sum"),
            Conversions=("Conversions", "sum"),
            Clicks=("Clicks", "sum")
        ).reset_index()

        # Calculate marketing performance metrics
        platform_budget["ROAS"] = (
            platform_budget["Revenue_BDT"] /
            platform_budget["Spend_BDT"].replace(0, np.nan)
        )

        platform_budget["CPA_BDT"] = (
            platform_budget["Spend_BDT"] /
            platform_budget["Conversions"].replace(0, np.nan)
        )

        total_spend = platform_budget["Spend_BDT"].sum()
        total_revenue = platform_budget["Revenue_BDT"].sum()
        total_conversions = platform_budget["Conversions"].sum()

        overall_roas = (
            total_revenue / total_spend if total_spend > 0 else np.nan
        )

        overall_cpa = (
            total_spend / total_conversions
            if total_conversions > 0 else np.nan
        )

        platform_budget["Budget_Share"] = (
            platform_budget["Spend_BDT"] / total_spend * 100
            if total_spend > 0 else 0
        )

        platform_budget["Revenue_Share"] = (
            platform_budget["Revenue_BDT"] / total_revenue * 100
            if total_revenue > 0 else 0
        )

        # Generate preliminary recommendations
        def recommend_action(row):
            if pd.isna(row["ROAS"]) or pd.isna(row["CPA_BDT"]):
                return "Insufficient conversion data"

            if row["ROAS"] >= overall_roas and row["CPA_BDT"] <= overall_cpa:
                return "Consider testing budget increases"

            elif row["ROAS"] < overall_roas and row["CPA_BDT"] > overall_cpa:
                return "Investigate campaign efficiency"

            else:
                return "Monitor and optimize"

        platform_budget["Recommendation"] = platform_budget.apply(
            recommend_action, axis=1
        )

        # Display overview metrics
        st.markdown("### Overall Marketing Performance")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Advertising Spend", f"BDT {total_spend:,.0f}")
        col2.metric("Overall ROAS", f"{overall_roas:.2f}x" if pd.notna(overall_roas) else "N/A")
        col3.metric("Overall CPA", f"BDT {overall_cpa:,.2f}" if pd.notna(overall_cpa) else "N/A")

        # Platform ROAS comparison
        st.markdown("### Return on Ad Spend by Platform")

        fig = px.bar(
            platform_budget.sort_values("ROAS", ascending=False),
            x="Platform",
            y="ROAS",
            color="Platform",
            title="Platform ROAS Comparison"
        )

        if pd.notna(overall_roas):
            fig.add_hline(
                y=overall_roas,
                line_dash="dash",
                annotation_text="Overall ROAS"
            )

        st.plotly_chart(fig, use_container_width=True)

        # Budget allocation
        st.markdown("### Advertising Budget Distribution")

        fig = px.pie(
            platform_budget,
            names="Platform",
            values="Spend_BDT",
            title="Share of Advertising Spend",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)

        # Recommendations table
        st.markdown("### Platform-Level Recommendations")

        st.dataframe(
            platform_budget[
                [
                    "Platform",
                    "Spend_BDT",
                    "Budget_Share",
                    "Revenue_BDT",
                    "Revenue_Share",
                    "ROAS",
                    "CPA_BDT",
                    "Recommendation"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Note: Recommendations are preliminary performance signals based "
            "on simulated data. Higher ROAS does not automatically mean higher "
            "profitability. Consider margins, attribution, conversion quality, "
            "and campaign scale before reallocating actual budgets."
        )
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
# REPORT DOWNLOAD CENTER
# ==========================================

st.divider()

st.header("Report Download Center")

st.write(
    "Download your filtered marketing campaign data "
    "and performance analysis."
)

# Prepare campaign report
campaign_report = filtered_df.copy()

# Prepare platform report
platform_report = filtered_df.groupby("Platform").agg(
    Impressions=("Impressions", "sum"),
    Clicks=("Clicks", "sum"),
    Spend_BDT=("Spend_BDT", "sum"),
    Conversions=("Conversions", "sum"),
    Revenue_BDT=("Revenue_BDT", "sum")
).reset_index()

platform_report["ROAS"] = (
    platform_report["Revenue_BDT"] /
    platform_report["Spend_BDT"].replace(0, np.nan)
)

platform_report["CPA_BDT"] = (
    platform_report["Spend_BDT"] /
    platform_report["Conversions"].replace(0, np.nan)
)

# Prepare audience report
audience_report = filtered_df.groupby("Audience_Segment").agg(
    Impressions=("Impressions", "sum"),
    Clicks=("Clicks", "sum"),
    Spend_BDT=("Spend_BDT", "sum"),
    Conversions=("Conversions", "sum"),
    Revenue_BDT=("Revenue_BDT", "sum")
).reset_index()

audience_report["ROAS"] = (
    audience_report["Revenue_BDT"] /
    audience_report["Spend_BDT"].replace(0, np.nan)
)

audience_report["CPA_BDT"] = (
    audience_report["Spend_BDT"] /
    audience_report["Conversions"].replace(0, np.nan)
)

# CSV download
col1, col2 = st.columns(2)

with col1:
    csv_data = campaign_report.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Campaign Report (CSV)",
        data=csv_data,
        file_name="campaign_performance_report.csv",
        mime="text/csv",
        use_container_width=True
    )

# Excel download
with col2:
    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        campaign_report.to_excel(
            writer,
            sheet_name="Campaign Data",
            index=False
        )

        platform_report.to_excel(
            writer,
            sheet_name="Platform Analysis",
            index=False
        )

        audience_report.to_excel(
            writer,
            sheet_name="Audience Analysis",
            index=False
        )
    # Professional Excel formatting

    for worksheet in writer.sheets.values():

        # Format header row
        for cell in worksheet[1]:
            cell.font = Font(
                bold=True,
                color="FFFFFF",
                size=11
            )

            cell.fill = PatternFill(
                start_color="1F4E78",
                end_color="1F4E78",
                fill_type="solid"
            )

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

        # Automatically adjust column widths
        for column_cells in worksheet.columns:
            max_length = 0
            column_letter = get_column_letter(
                column_cells[0].column
            )

            for cell in column_cells:
                if cell.value is not None:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

            worksheet.column_dimensions[column_letter].width = min(
                max_length + 3, 30
            )

        # Freeze header row
        worksheet.freeze_panes = "A2"

        # Enable Excel filters
        worksheet.auto_filter.ref = worksheet.dimensions

        # Format financial and performance metrics
        for column_cells in worksheet.columns:
            header = str(column_cells[0].value)

            for cell in column_cells[1:]:

                if header in ["Spend_BDT", "Revenue_BDT", "CPA_BDT"]:
                    cell.number_format = '"BDT "#,##0.00'

                elif header in ["CTR", "Conversion_Rate"]:
                    cell.number_format = '0.00"%"'

                elif header == "ROAS":
                    cell.number_format = '0.00"x"'

                elif header in ["Impressions", "Clicks", "Conversions"]:
                    cell.number_format = '#,##0'
    excel_data = excel_buffer.getvalue()

    st.download_button(
        label="Download Full Report (Excel)",
        data=excel_data,
        file_name="marketing_performance_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

st.caption(
    "Reports reflect the currently selected dashboard filters. "
    "All data in this project is simulated."
)

# ==========================================
# 13. FOOTER
# ==========================================

st.divider()

st.caption(
    "Marketing Campaign Performance Analyzer | "

    "Portfolio Project"
)

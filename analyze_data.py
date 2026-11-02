
import pandas as pd
import numpy as np

# 1. Load the dataset
df = pd.read_csv("data/campaigns.csv")

# 2. Convert Date column into a proper date format
df["Date"] = pd.to_datetime(df["Date"])

print("\n========== DATASET OVERVIEW ==========")

# 3. Check the dataset dimensions
print("Number of rows and columns:", df.shape)

# 4. Check column information
print("\nColumn information:")
print(df.info())

# 5. Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# 6. Calculate marketing performance metrics
df["CTR"] = (df["Clicks"] / df["Impressions"]) * 100

df["CPC_BDT"] = np.where(
    df["Clicks"] > 0,
    df["Spend_BDT"] / df["Clicks"],
    0
)

df["Conversion_Rate"] = np.where(
    df["Clicks"] > 0,
    (df["Conversions"] / df["Clicks"]) * 100,
    0
)

df["CPA_BDT"] = np.where(
    df["Conversions"] > 0,
    df["Spend_BDT"] / df["Conversions"],
    0
)

df["ROAS"] = np.where(
    df["Spend_BDT"] > 0,
    df["Revenue_BDT"] / df["Spend_BDT"],
    0
)

# 7. Group performance by advertising platform
platform_summary = df.groupby("Platform").agg({
    "Impressions": "sum",
    "Clicks": "sum",
    "Spend_BDT": "sum",
    "Conversions": "sum",
    "Revenue_BDT": "sum"
})

# Calculate weighted metrics using platform totals
platform_summary["CTR"] = (
    platform_summary["Clicks"] /
    platform_summary["Impressions"] * 100
)

platform_summary["CPC_BDT"] = (
    platform_summary["Spend_BDT"] /
    platform_summary["Clicks"]
)

platform_summary["Conversion_Rate"] = (
    platform_summary["Conversions"] /
    platform_summary["Clicks"] * 100
)

platform_summary["CPA_BDT"] = (
    platform_summary["Spend_BDT"] /
    platform_summary["Conversions"]
)

platform_summary["ROAS"] = (
    platform_summary["Revenue_BDT"] /
    platform_summary["Spend_BDT"]
)

print("\n========== PLATFORM PERFORMANCE ==========")
print(platform_summary.round(2))

# 8. Identify the platform with the highest ROAS
best_platform = platform_summary["ROAS"].idxmax()

print("\nBest platform by ROAS:", best_platform)

# 9. Identify the platform with the lowest CPA
lowest_cpa_platform = platform_summary["CPA_BDT"].idxmin()

print("Lowest acquisition cost platform:", lowest_cpa_platform)

# 10. Identify the highest revenue campaign
campaign_summary = df.groupby(
    ["Campaign_ID", "Campaign_Name", "Platform"]
).agg({
    "Spend_BDT": "sum",
    "Conversions": "sum",
    "Revenue_BDT": "sum"
})

campaign_summary["ROAS"] = (
    campaign_summary["Revenue_BDT"] /
    campaign_summary["Spend_BDT"]
)

top_campaign = campaign_summary["Revenue_BDT"].idxmax()

print("\nHighest revenue campaign:")
print(top_campaign)

print(
    "\nTotal revenue generated:",
    round(df["Revenue_BDT"].sum(), 2),
    "BDT"
)

print(
    "Total advertising expenditure:",
    round(df["Spend_BDT"].sum(), 2),
    "BDT"
)

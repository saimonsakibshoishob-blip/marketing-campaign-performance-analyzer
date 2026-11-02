
import pandas as pd
import numpy as np
from pathlib import Path

# 1. Set up a random number generator
rng = np.random.default_rng(42)

# 2. Define advertising platforms and their characteristics
platforms = {
    "Facebook": {
        "cpm": 180,
        "ctr": 0.035,
        "conversion_rate": 0.055,
        "average_order_value": 1200
    },
    "Instagram": {
        "cpm": 220,
        "ctr": 0.045,
        "conversion_rate": 0.060,
        "average_order_value": 1400
    },
    "Google Ads": {
        "cpm": 300,
        "ctr": 0.065,
        "conversion_rate": 0.085,
        "average_order_value": 1800
    },
    "YouTube": {
        "cpm": 120,
        "ctr": 0.020,
        "conversion_rate": 0.025,
        "average_order_value": 1100
    }
}

# 3. Define campaign names and objectives
campaigns = [
    ("New Year Sale", "Sales"),
    ("Brand Awareness", "Awareness"),
    ("Winter Collection", "Sales"),
    ("Website Traffic", "Traffic"),
    ("Retargeting Campaign", "Retargeting")
]

audiences = [
    "Students",
    "Young Professionals",
    "Families",
    "Online Shoppers"
]

# 4. Create 365 days of possible reporting dates
all_dates = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    freq="D"
)

records = []

# 5. Generate 20 reporting dates for each campaign on each platform
for platform, settings in platforms.items():

    for campaign_number, (campaign_name, objective) in enumerate(campaigns, start=1):

        campaign_id = f"{platform[:3].upper()}-C{campaign_number:02d}"

        selected_dates = rng.choice(
            all_dates,
            size=20,
            replace=False
        )

        for date in selected_dates:

            impressions = int(rng.integers(10000, 100001))

            # Calculate clicks
            clicks = int(rng.binomial(
                impressions,
                settings["ctr"]
            ))

            # Calculate conversions
            conversions = int(rng.binomial(
                clicks,
                settings["conversion_rate"]
            ))

            # Calculate advertising expenditure
            spend = (
                impressions / 1000
                * settings["cpm"]
                * rng.uniform(0.85, 1.15)
            )

            # Calculate attributed revenue
            revenue = (
                conversions
                * settings["average_order_value"]
                * rng.uniform(0.80, 1.20)
            )

            records.append({
                "Date": date,
                "Campaign_ID": campaign_id,
                "Campaign_Name": campaign_name,
                "Platform": platform,
                "Objective": objective,
                "Audience_Segment": rng.choice(audiences),
                "Impressions": impressions,
                "Clicks": clicks,
                "Spend_BDT": round(spend, 2),
                "Conversions": conversions,
                "Revenue_BDT": round(revenue, 2)
            })

# 6. Convert records into a Pandas DataFrame
df = pd.DataFrame(records)

# 7. Sort the dataset by date
df = df.sort_values("Date").reset_index(drop=True)

# 8. Create the data folder if it doesn't exist
Path("data").mkdir(exist_ok=True)

# 9. Export the dataset to CSV
df.to_csv("data/campaigns.csv", index=False)

print("Marketing dataset successfully created!")
print(f"Total records: {len(df)}")
print(f"Total campaigns: {df['Campaign_ID'].nunique()}")
print(f"Platforms: {df['Platform'].nunique()}")
print("Saved to: data/campaigns.csv")

print("\nFirst five records:")
print(df.head())

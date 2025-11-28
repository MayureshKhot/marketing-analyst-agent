import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Number of rows
N = 1000

# Generate dates (past 200 days)
start_date = datetime.today() - timedelta(days=200)
dates = [start_date + timedelta(days=i) for i in range(200)]
date_col = random.choices(dates, k=N)

channels = ["Google", "Meta", "YouTube", "Email", "Organic", "Referral"]
campaigns = [
    "Brand Search", "Retargeting", "Cold Prospecting",
    "Video Awareness", "Email Blast", "Sale Promo"
]
devices = ["mobile", "desktop"]
countries = ["India", "USA", "UK", "Canada", "Australia"]

data = {
    "date": [d.strftime("%Y-%m-%d") for d in date_col],
    "channel": [random.choice(channels) for _ in range(N)],
    "campaign": [random.choice(campaigns) for _ in range(N)],
    "device": [random.choice(devices) for _ in range(N)],
    "geo": [random.choice(countries) for _ in range(N)],
}

# Generate impressions
data["impressions"] = np.random.randint(100, 50000, N)

# Generate clicks dependent on impressions
data["clicks"] = (data["impressions"] * np.random.uniform(0.01, 0.2, N)).astype(int)

# Generate spend dependent on clicks
data["spend"] = np.round(data["clicks"] * np.random.uniform(2, 10, N), 2)

# Generate conversions dependent on clicks
data["conversions"] = (data["clicks"] * np.random.uniform(0.01, 0.2, N)).astype(int)

# Generate revenue dependent on conversions
data["revenue"] = np.round(data["conversions"] * np.random.uniform(20, 150, N), 2)

df = pd.DataFrame(data)

# Save CSV
output_path = "data/demo_marketing_data.csv"
df.to_csv(output_path, index=False)

print(f"Dataset created: {output_path}")
print(df.head())

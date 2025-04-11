from pathlib import Path

import pandas as pd

# Load data
csv_path = Path("../data/raw/merged_log_ibutton_data_2025_04_10.csv")
df = pd.read_csv(csv_path, parse_dates=["datetime"])

# Extract hour from datetime
df["hour"] = df["datetime"].dt.hour

# Create day/night column
df["day_period"] = df["hour"].apply(lambda h: "day" if 6 <= h < 18 else "night")

# Group and compute DTR for each group by period
dtr = (
    df.groupby(["structure", "surface", "location", "arm", "comparable_structure", "day_period"])["value"]
    .agg(["min", "max"])
    .reset_index()
)
dtr["dtr"] = dtr["max"] - dtr["min"]

# Pivot to get daytime and nighttime DTR side-by-side
dtr_pivot = dtr.pivot_table(
    index=["structure", "surface", "location", "arm", "comparable_structure"],
    columns="day_period",
    values="dtr"
).reset_index()

# Rename columns for clarity
dtr_pivot.columns.name = None
dtr_pivot = dtr_pivot.rename(columns={"day": "dtr_daytime", "night": "dtr_nighttime"})

# Save to processed folder
output_path = Path("../data/processed/dtr_by_structure.csv")
dtr_pivot.to_csv(output_path, index=False)

print(f"✅ DTR summary saved to: {output_path}")

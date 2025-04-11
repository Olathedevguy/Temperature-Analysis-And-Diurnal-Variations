from pathlib import Path

import pandas as pd

# Load the CSV
df = pd.read_csv("../data/raw/merged_log_ibutton_data_2025_04_10.csv", parse_dates=["datetime"])

# Add hour and period column
df["hour"] = df["datetime"].dt.hour
df["period"] = df["hour"].apply(lambda h: "day" if 6 <= h < 18 else "night")

# Group and compute DTR per structure/period
dtr = (
    df.groupby(["structure", "surface", "location", "arm", "comparable_structure", "period"])["value"]
    .agg(["min", "max"])
    .reset_index()
)
dtr["dtr"] = dtr["max"] - dtr["min"]

# Pivot to wide format (day/night in columns)
dtr_wide = dtr.pivot_table(
    index=["structure", "surface", "location", "arm", "comparable_structure"],
    columns="period",
    values="dtr"
).reset_index().rename(columns={"day": "dtr_daytime", "night": "dtr_nighttime"})

# Split into case and control
case = dtr_wide[dtr_wide["arm"] == "Case"]
control = dtr_wide[dtr_wide["arm"] == "Control"]

print(case.head())
# Merge based on matching rules
matched = pd.merge(
    case,
    control,
    right_on=["comparable_structure", "surface", "location"],
    left_on=["structure", "surface", "location"],
    suffixes=("_case", "_control")
)

# Select & rename for clarity
final = matched[[
    "structure_case", "structure_control",
    "surface", "location",
    "dtr_daytime_case", "dtr_daytime_control",
    "dtr_nighttime_case", "dtr_nighttime_control"
]]

# Save output
output_path = Path("../data/processed/matched_dtr_pairs.csv")
final.to_csv(output_path, index=False)

print(f"✅ Matched DTR pairs saved to: {output_path}")

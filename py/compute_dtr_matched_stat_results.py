from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ttest_rel

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

final = matched[[
    "structure_case", "structure_control",
    "surface", "location",
    "dtr_daytime_case", "dtr_daytime_control",
    "dtr_nighttime_case", "dtr_nighttime_control"
]].copy()  # 👈 Add .copy() here

# Now you're safe to assign without warnings
final["dtr_day_diff"] = final["dtr_daytime_case"] - final["dtr_daytime_control"]
final["dtr_night_diff"] = final["dtr_nighttime_case"] - final["dtr_nighttime_control"]

# Paired t-test
t_day, p_day = ttest_rel(final["dtr_daytime_case"], final["dtr_daytime_control"])
t_night, p_night = ttest_rel(final["dtr_nighttime_case"], final["dtr_nighttime_control"])


# Confidence Intervals
def conf_interval(data, confidence=0.95):
    mean = np.mean(data)
    std_err = np.std(data, ddof=1) / np.sqrt(len(data))
    margin = 1.96 * std_err
    return mean, mean - margin, mean + margin


# Add summary row (one-row DataFrame for stats)
summary_df = pd.DataFrame([{
    "structure_case": "Summary",
    "structure_control": "",
    "surface": "",
    "location": "Overall",
    "dtr_daytime_case": final["dtr_daytime_case"].mean(),
    "dtr_daytime_control": final["dtr_daytime_control"].mean(),
    "dtr_nighttime_case": final["dtr_nighttime_case"].mean(),
    "dtr_nighttime_control": final["dtr_nighttime_control"].mean(),
    "dtr_day_diff": final["dtr_day_diff"].mean(),
    "dtr_night_diff": final["dtr_night_diff"].mean(),
    "dtr_day_diff_ci_lower": conf_interval(final["dtr_day_diff"])[1],
    "dtr_day_diff_ci_upper": conf_interval(final["dtr_day_diff"])[2],
    "dtr_day_p_value": p_day,
    "dtr_night_diff_ci_lower": conf_interval(final["dtr_night_diff"])[1],
    "dtr_night_diff_ci_upper": conf_interval(final["dtr_night_diff"])[2],
    "dtr_night_p_value": p_night,
}])

# Combine
final_with_summary = pd.concat([final, summary_df], ignore_index=True)

# Save to file
output_path = Path("../data/processed/matched_dtr_pairs_with_stats.csv")
final_with_summary.to_csv(output_path, index=False)

print(f"📁 Final file with stats saved to: {output_path}")

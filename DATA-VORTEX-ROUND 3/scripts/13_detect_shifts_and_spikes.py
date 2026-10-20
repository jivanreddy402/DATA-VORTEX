import pandas as pd
from pathlib import Path

INPUT_FILE = Path(
    "data/processed/meta_one_round3_sentiment.csv"
)

OUTPUT_FILE = Path(
    "data/processed/meta_one_round3_shift_analysis.csv"
)

# --------------------------------------------------
# LOAD
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True
)

df["date"] = df["published_at"].dt.date

# --------------------------------------------------
# DAILY SENTIMENT
# --------------------------------------------------

daily = (
    df.groupby(["date", "predicted_sentiment"])
      .size()
      .unstack(fill_value=0)
      .reset_index()
)

for sentiment in ["Negative", "Neutral", "Positive"]:
    if sentiment not in daily.columns:
        daily[sentiment] = 0

daily["total"] = (
    daily["Negative"]
    + daily["Neutral"]
    + daily["Positive"]
)

# --------------------------------------------------
# PERCENTAGES
# --------------------------------------------------

daily["negative_pct"] = (
    daily["Negative"] / daily["total"] * 100
)

daily["neutral_pct"] = (
    daily["Neutral"] / daily["total"] * 100
)

daily["positive_pct"] = (
    daily["Positive"] / daily["total"] * 100
)

daily["dominant_sentiment"] = daily[
    ["Negative", "Neutral", "Positive"]
].idxmax(axis=1)

# --------------------------------------------------
# DAY-TO-DAY CHANGES
# --------------------------------------------------

daily["positive_change_pp"] = (
    daily["positive_pct"].diff()
)

daily["neutral_change_pp"] = (
    daily["neutral_pct"].diff()
)

daily["negative_change_pp"] = (
    daily["negative_pct"].diff()
)

daily["activity_change"] = daily["total"].diff()

# --------------------------------------------------
# ACTIVITY SPIKE
# --------------------------------------------------

mean_activity = daily["total"].mean()
std_activity = daily["total"].std()

daily["activity_zscore"] = (
    (daily["total"] - mean_activity) / std_activity
)

daily["activity_spike"] = (
    daily["activity_zscore"] >= 1
)

# --------------------------------------------------
# SAVE
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

daily.to_csv(
    OUTPUT_FILE,
    index=False
)

# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

print("=" * 75)
print("ROUND 3 SHIFT + ACTIVITY ANALYSIS")
print("=" * 75)

print(
    daily[
        [
            "date",
            "Negative",
            "Neutral",
            "Positive",
            "total",
            "dominant_sentiment",
            "negative_change_pp",
            "neutral_change_pp",
            "positive_change_pp",
            "activity_change",
            "activity_zscore",
            "activity_spike"
        ]
    ].to_string(index=False)
)

print("\n" + "=" * 75)
print("LARGEST SENTIMENT MOVEMENTS")
print("=" * 75)

changes = daily.iloc[1:].copy()

changes["largest_change_pp"] = changes[
    [
        "negative_change_pp",
        "neutral_change_pp",
        "positive_change_pp"
    ]
].abs().max(axis=1)

print(
    changes[
        [
            "date",
            "negative_change_pp",
            "neutral_change_pp",
            "positive_change_pp",
            "largest_change_pp"
        ]
    ]
    .sort_values("largest_change_pp", ascending=False)
    .to_string(index=False)
)

print("\n" + "=" * 75)
print("ACTIVITY SPIKES")
print("=" * 75)

spikes = daily[daily["activity_spike"]]

if len(spikes) == 0:
    print("No statistical activity spike detected using z-score >= 1.")
else:
    print(
        spikes[
            ["date", "total", "activity_zscore"]
        ].to_string(index=False)
    )

print("\nSaved to:")
print(OUTPUT_FILE)

print("=" * 75)
import pandas as pd
from pathlib import Path

INPUT_FILE = Path(
    "data/processed/meta_one_round3_sentiment.csv"
)

OUTPUT_FILE = Path(
    "data/processed/meta_one_sentiment_daily.csv"
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
# DAILY SENTIMENT COUNTS
# --------------------------------------------------

daily = (
    df.groupby(["date", "predicted_sentiment"])
      .size()
      .unstack(fill_value=0)
      .reset_index()
)

# Ensure all sentiment columns exist
for sentiment in ["Negative", "Neutral", "Positive"]:
    if sentiment not in daily.columns:
        daily[sentiment] = 0

# --------------------------------------------------
# DAILY TOTAL + DOMINANT SENTIMENT
# --------------------------------------------------

daily["total_records"] = (
    daily["Negative"]
    + daily["Neutral"]
    + daily["Positive"]
)

daily["dominant_sentiment"] = daily[
    ["Negative", "Neutral", "Positive"]
].idxmax(axis=1)

# --------------------------------------------------
# SENTIMENT PERCENTAGES
# --------------------------------------------------

daily["negative_pct"] = (
    daily["Negative"] / daily["total_records"] * 100
)

daily["neutral_pct"] = (
    daily["Neutral"] / daily["total_records"] * 100
)

daily["positive_pct"] = (
    daily["Positive"] / daily["total_records"] * 100
)

# --------------------------------------------------
# SORT
# --------------------------------------------------

daily = daily.sort_values("date").reset_index(drop=True)

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

print("=" * 70)
print("ROUND 3 DAILY SENTIMENT TIMELINE")
print("=" * 70)

print(
    daily[
        [
            "date",
            "Negative",
            "Neutral",
            "Positive",
            "total_records",
            "dominant_sentiment",
            "negative_pct",
            "neutral_pct",
            "positive_pct"
        ]
    ].to_string(index=False)
)

print("\n" + "=" * 70)
print("DOMINANT SENTIMENT CHANGES")
print("=" * 70)

previous = None

for _, row in daily.iterrows():

    current = row["dominant_sentiment"]

    if previous is not None and current != previous:
        print(
            f"{row['date']}: "
            f"{previous} → {current}"
        )

    previous = current

print("\nSaved to:")
print(OUTPUT_FILE)

print("=" * 70)
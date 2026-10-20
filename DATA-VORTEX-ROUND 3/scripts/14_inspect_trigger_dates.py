import pandas as pd
from pathlib import Path

INPUT_FILE = Path(
    "data/processed/meta_one_round3_sentiment.csv"
)

df = pd.read_csv(INPUT_FILE)

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True
)

df["date"] = df["published_at"].dt.date

TARGET_DATES = [
    "2026-09-16",
    "2026-09-18",
    "2026-09-20"
]

for target in TARGET_DATES:

    date = pd.Timestamp(target).date()

    subset = df[df["date"] == date].copy()

    print("\n")
    print("=" * 90)
    print(f"TRIGGER DATE: {date}")
    print(f"RECORDS: {len(subset)}")
    print("=" * 90)

    if len(subset) == 0:
        print("No records.")
        continue

    print(
        subset[
            [
                "platform",
                "source",
                "content_type",
                "published_at",
                "predicted_sentiment",
                "sentiment_confidence",
                "text",
                "source_url"
            ]
        ].to_string(index=False)
    )
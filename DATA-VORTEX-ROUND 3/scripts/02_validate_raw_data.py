import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data/raw/meta_one_news_raw.csv")

print("=" * 70)
print("ROUND 3 — RAW DATA VALIDATION")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

print(f"\nTotal records: {len(df)}")
print(f"Columns: {list(df.columns)}")

# ------------------------------------------------------------
# Date analysis
# ------------------------------------------------------------

df["published_at_utc"] = pd.to_datetime(
    df["published_at_utc"],
    utc=True
)

print("\n" + "-" * 70)
print("RECORDS BY DATE")
print("-" * 70)

date_counts = (
    df["published_at_utc"]
    .dt.date
    .value_counts()
    .sort_index()
)

print(date_counts.to_string())

# ------------------------------------------------------------
# Unique values
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("UNIQUENESS CHECK")
print("-" * 70)

print("Total records:", len(df))
print("Unique titles:", df["title"].nunique())
print("Unique links:", df["link"].nunique())
print("Unique sources:", df["source"].nunique())

# ------------------------------------------------------------
# Source distribution
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("TOP SOURCES")
print("-" * 70)

print(
    df["source"]
    .value_counts()
    .head(20)
    .to_string()
)

# ------------------------------------------------------------
# Show titles
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("ALL COLLECTED TITLES")
print("-" * 70)

for i, title in enumerate(df["title"], start=1):
    print(f"{i:03d}. {title}")

# ------------------------------------------------------------
# Search for suspicious/unrelated terms
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("POSSIBLY UNRELATED RECORDS")
print("-" * 70)

suspicious_terms = [
    "meta quest",
    "quest 2",
    "quest 3",
    "quest 3s",
    "ray-ban",
    "ray ban",
    "smart glasses",
    "wayfarer",
    "viture",
]

pattern = "|".join(suspicious_terms)

suspicious = df[
    df["title"]
    .str.lower()
    .str.contains(pattern, regex=True, na=False)
]

print(f"Suspicious records found: {len(suspicious)}")

if len(suspicious) > 0:
    print(
        suspicious[
            ["published_at_utc", "title", "source"]
        ].to_string(index=False)
    )

# ------------------------------------------------------------
# Save validation report
# ------------------------------------------------------------

report_dir = Path("reports")
report_dir.mkdir(parents=True, exist_ok=True)

date_counts.to_csv(
    report_dir / "raw_records_by_date.csv",
    header=["record_count"]
)

print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
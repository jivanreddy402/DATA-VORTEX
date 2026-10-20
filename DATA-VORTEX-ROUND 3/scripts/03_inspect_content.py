import pandas as pd

FILE = "data/raw/meta_one_news_raw.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("ROUND 3 — CONTENT QUALITY INSPECTION")
print("=" * 70)

print("\nTOTAL RECORDS:", len(df))

# ------------------------------------------------------------
# Summary length
# ------------------------------------------------------------

df["title"] = df["title"].fillna("")
df["summary"] = df["summary"].fillna("")

df["title_length"] = df["title"].str.len()
df["summary_length"] = df["summary"].str.len()

print("\n" + "-" * 70)
print("SUMMARY LENGTH")
print("-" * 70)

print(df["summary_length"].describe())

# ------------------------------------------------------------
# Empty summaries
# ------------------------------------------------------------

empty_summary = (df["summary_length"] == 0).sum()

print("\nEmpty summaries:", empty_summary)

# ------------------------------------------------------------
# Sample records
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("SAMPLE RECORDS")
print("-" * 70)

for i, row in df.head(10).iterrows():

    print(f"\nRECORD {i + 1}")
    print("TITLE:")
    print(row["title"])

    print("\nSUMMARY:")
    print(row["summary"])

    print("\nSOURCE:")
    print(row["source"])

    print("\nPUBLISHED:")
    print(row["published_at_utc"])

    print("\n" + "-" * 50)

# ------------------------------------------------------------
# Longest summaries
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("LONGEST SUMMARIES")
print("-" * 70)

longest = df.sort_values(
    "summary_length",
    ascending=False
).head(10)

for _, row in longest.iterrows():

    print("\nTITLE:", row["title"])
    print("SUMMARY LENGTH:", row["summary_length"])
    print("SUMMARY:", row["summary"][:500])

# ------------------------------------------------------------
# Google News wrapper detection
# ------------------------------------------------------------

wrapper_terms = [
    "google news",
    "news.google.com",
    "read more",
    "click here"
]

print("\n" + "-" * 70)
print("POSSIBLE RSS WRAPPERS")
print("-" * 70)

wrapper_mask = df["summary"].str.lower().apply(
    lambda x: any(term in x for term in wrapper_terms)
)

print("Possible wrapper summaries:", wrapper_mask.sum())

print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)
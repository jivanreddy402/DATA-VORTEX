import pandas as pd
from pathlib import Path

INPUT = Path("data/raw/meta_one_reddit_public.csv")

df = pd.read_csv(INPUT)

print("=" * 60)
print("REDDIT DATASET VALIDATION")
print("=" * 60)

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())

print("\nContent types:")
print(df["content_type"].value_counts())

print("\nSubreddits:")
print(df["subreddit"].value_counts())

print("\nDate distribution:")
print(df["published_at"].value_counts().sort_index())

print("\nSample records:")
print(df[["platform", "subreddit", "content_type", "text", "published_at"]].head(10).to_string(index=False))

print("\n" + "=" * 60)
print("VALIDATION COMPLETE")
print("=" * 60)
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# INPUT FILES
# --------------------------------------------------

REDDIT_FILE = Path("data/raw/meta_one_reddit_public.csv")
NEWS_FILE = Path("data/raw/meta_one_news_raw.csv")

OUTPUT_FILE = Path("data/processed/meta_one_round3_unified.csv")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

reddit = pd.read_csv(REDDIT_FILE)
news = pd.read_csv(NEWS_FILE)

print("=" * 60)
print("BUILDING ROUND 3 UNIFIED DATASET")
print("=" * 60)

print(f"Reddit records : {len(reddit)}")
print(f"News records   : {len(news)}")


# --------------------------------------------------
# STANDARDIZE REDDIT
# --------------------------------------------------

reddit_unified = pd.DataFrame({
    "record_id": reddit["record_id"],
    "platform": "Reddit",
    "source": reddit["subreddit"],
    "content_type": reddit["content_type"],
    "text": reddit["text"],
    "published_at": pd.to_datetime(
        reddit["published_at"], errors="coerce"
    ),
    "engagement_score": pd.to_numeric(
        reddit["score"], errors="coerce"
    ),
    "source_url": reddit["source_url"],
    "collection_method": reddit["collection_method"]
})


# --------------------------------------------------
# STANDARDIZE NEWS
# --------------------------------------------------

news_unified = pd.DataFrame({
    "record_id": [
        f"news_{i+1:04d}"
        for i in range(len(news))
    ],
    "platform": "News",
    "source": news["source"],
    "content_type": "article",
    "text": (
        news["title"].fillna("").astype(str)
        + " "
        + news["summary"].fillna("").astype(str)
    ).str.strip(),
    "published_at": pd.to_datetime(
        news["published_at_utc"], errors="coerce"
    ),
    "engagement_score": None,
    "source_url": news["link"],
    "collection_method": "Google News RSS"
})


# --------------------------------------------------
# COMBINE
# --------------------------------------------------

unified = pd.concat(
    [reddit_unified, news_unified],
    ignore_index=True
)


# --------------------------------------------------
# CLEAN
# --------------------------------------------------

unified["text"] = (
    unified["text"]
    .fillna("")
    .astype(str)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

unified["published_at"] = pd.to_datetime(
    unified["published_at"],
    errors="coerce",
    utc=True
)

unified = unified.drop_duplicates(
    subset=["platform", "source_url", "text"]
)

unified = unified.sort_values(
    "published_at"
).reset_index(drop=True)


# --------------------------------------------------
# SAVE
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

unified.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# REPORT
# --------------------------------------------------

print("\nUnified dataset:")
print(f"Records       : {len(unified)}")
print(f"Columns       : {len(unified.columns)}")

print("\nPlatform distribution:")
print(unified["platform"].value_counts())

print("\nContent types:")
print(unified["content_type"].value_counts())

print("\nMissing values:")
print(unified.isnull().sum())

print("\nDate range:")
print(
    unified["published_at"].min(),
    "→",
    unified["published_at"].max()
)

print("\nSaved to:")
print(OUTPUT_FILE)

print("=" * 60)
print("UNIFIED DATASET CREATED")
print("=" * 60)
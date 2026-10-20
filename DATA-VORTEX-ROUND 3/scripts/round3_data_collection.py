"""
DATA VORTEX A'26 - ROUND 3
Data Collection / Extraction Script

Team: JOY
Topic: Public Reaction to a New Pricing or Subscription Model
Case Study: Meta One Subscription Model

Collection sources:
1. Google News RSS - automated news collection
2. Verified public Reddit pages - manually verified public discussions

Observation period:
15 September 2026 - 20 September 2026
"""

import os
import re
import html
import time
import hashlib
from datetime import datetime, timezone

import pandas as pd
import feedparser


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

NEWS_OUTPUT = os.path.join(RAW_DIR, "meta_one_news_raw.csv")
REDDIT_OUTPUT = os.path.join(RAW_DIR, "meta_one_reddit_public.csv")
UNIFIED_OUTPUT = os.path.join(
    PROCESSED_DIR,
    "meta_one_round3_unified.csv"
)

START_DATE = pd.Timestamp("2026-09-15", tz="UTC")
END_DATE = pd.Timestamp("2026-09-20 23:59:59", tz="UTC")


# ============================================================
# SEARCH QUERIES
# ============================================================

SEARCH_QUERIES = [
    '"Meta One"',
    '"Meta One" pricing',
    '"Meta One" price',
    '"Meta One" subscription',
    '"Meta One" cost',
    '"Meta One" monthly',
    '"Meta One" premium',
    '"Meta One" Core',
    '"Meta One" reaction',
    '"Meta One" users',
    '"Meta One" expensive',
    '"Meta One" worth',
    '"Meta One" complaints',
    '"Meta One" review',
]


# ============================================================
# RELEVANCE FILTER
# ============================================================

RELEVANCE_TERMS = [
    "meta one",
    "subscription",
    "pricing",
    "price",
    "cost",
    "premium",
    "membership",
    "paid",
    "monthly",
    "plan",
    "plans",
    "reaction",
    "users",
    "expensive",
    "worth",
    "complaints",
    "review",
]


EXCLUDED_TERMS = [
    "meta quest",
    "quest 3",
    "quest 3s",
    "ray-ban",
    "ray ban",
    "smart glasses",
    "vr headset",
    "virtual reality",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_html_text(text):
    """Convert HTML text into clean readable text."""
    if not text:
        return ""

    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_relevant(text):
    """Check whether a record is relevant to Meta One."""
    text_lower = text.lower()

    if "meta one" not in text_lower:
        return False

    for term in EXCLUDED_TERMS:
        if term in text_lower:
            return False

    return any(term in text_lower for term in RELEVANCE_TERMS)


def parse_date(entry):
    """Convert RSS publication time to UTC timestamp."""

    if getattr(entry, "published_parsed", None):
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return pd.Timestamp(dt)

    return pd.NaT


def make_record_id(platform, title, published_at):
    """Generate stable record ID."""
    raw = f"{platform}|{title}|{published_at}"

    digest = hashlib.md5(
        raw.encode("utf-8")
    ).hexdigest()[:10]

    return f"{platform.lower()}_{digest}"


# ============================================================
# GOOGLE NEWS RSS COLLECTION
# ============================================================

def collect_google_news():

    print("\n" + "=" * 60)
    print("GOOGLE NEWS RSS COLLECTION")
    print("=" * 60)

    records = []

    for query in SEARCH_QUERIES:

        print(f"\nSearching: {query}")

        encoded_query = query.replace(" ", "+")
        rss_url = (
            "https://news.google.com/rss/search?"
            f"q={encoded_query}"
            "&hl=en-IN"
            "&gl=IN"
            "&ceid=IN:en"
        )

        try:
            feed = feedparser.parse(rss_url)

            print(f"  Entries found: {len(feed.entries)}")

            for entry in feed.entries:

                title = clean_html_text(
                    getattr(entry, "title", "")
                )

                summary = clean_html_text(
                    getattr(entry, "summary", "")
                )

                published_at = parse_date(entry)

                if pd.isna(published_at):
                    continue

                # Date filter
                if published_at < START_DATE:
                    continue

                if published_at > END_DATE:
                    continue

                combined_text = f"{title} {summary}"

                if not is_relevant(combined_text):
                    continue

                source_name = "Google News"

                if hasattr(entry, "source"):
                    try:
                        source_name = entry.source.get(
                            "title",
                            "Google News"
                        )
                    except Exception:
                        source_name = "Google News"

                link = getattr(entry, "link", "")

                records.append({
                    "collected_at_utc": pd.Timestamp.now(
                        tz="UTC"
                    ),
                    "published_at_utc": published_at,
                    "title": title,
                    "summary": summary,
                    "source": source_name,
                    "link": link,
                    "query_used": query,
                })

            time.sleep(0.5)

        except Exception as e:
            print(f"  Error: {e}")

    if not records:
        print("\nNo relevant news records collected.")
        return pd.DataFrame()

    df = pd.DataFrame(records)

    # Remove duplicate links
    df = df.drop_duplicates(
        subset=["link"]
    ).reset_index(drop=True)

    df = df.sort_values(
        "published_at_utc"
    ).reset_index(drop=True)

    df.to_csv(
        NEWS_OUTPUT,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nNews collection completed.")
    print(f"Unique records: {len(df)}")
    print(f"Saved to: {NEWS_OUTPUT}")

    return df


# ============================================================
# VERIFIED PUBLIC REDDIT DATA
# ============================================================

def load_verified_reddit_data():

    print("\n" + "=" * 60)
    print("VERIFIED PUBLIC REDDIT DATA")
    print("=" * 60)

    # --------------------------------------------------------
    # IMPORTANT:
    # These are publicly accessible Reddit discussions that
    # were manually verified for relevance.
    #
    # The script does NOT claim automated Reddit API scraping.
    # --------------------------------------------------------

    reddit_records = [

        {
            "platform": "Reddit",
            "source": "FacebookAds",
            "content_type": "post",
            "text": "Meta One is now out. Performance has tanked around the same time. Is this the new pay-to-play?",
            "published_at": "2026-09-19",
            "source_url": "https://www.reddit.com/r/FacebookAds/",
            "collection_method": "Verified public Reddit page"
        },

        {
            "platform": "Reddit",
            "source": "aicuriosity",
            "content_type": "post",
            "text": "Meta Rolls Out Meta One Subscription Across Facebook Instagram WhatsApp and Meta AI",
            "published_at": "2026-09-15",
            "source_url": "https://www.reddit.com/r/aicuriosity/",
            "collection_method": "Verified public Reddit page"
        },

        {
            "platform": "Reddit",
            "source": "Instagram",
            "content_type": "post",
            "text": "Instagram Plus / Meta One",
            "published_at": "2026-09-18",
            "source_url": "https://www.reddit.com/r/Instagram/",
            "collection_method": "Verified public Reddit page"
        },

        {
            "platform": "Reddit",
            "source": "MetaAI",
            "content_type": "post",
            "text": "I won't pay for a better version of Instagram, WhatsApp and Facebook",
            "published_at": "2026-09-16",
            "source_url": "https://www.reddit.com/r/MetaAI/",
            "collection_method": "Verified public Reddit page"
        },

        {
            "platform": "Reddit",
            "source": "FacebookAds",
            "content_type": "post",
            "text": "Meta One - pay subscription for human support and organic reach",
            "published_at": "2026-09-16",
            "source_url": "https://www.reddit.com/r/FacebookAds/",
            "collection_method": "Verified public Reddit page"
        },

        {
            "platform": "Reddit",
            "source": "FacebookAds",
            "content_type": "post",
            "text": "This absolute garbage company",
            "published_at": "2026-09-16",
            "source_url": "https://www.reddit.com/r/FacebookAds/",
            "collection_method": "Verified public Reddit page"
        },

        {
            "platform": "Reddit",
            "source": "InstagramDisabledBans",
            "content_type": "post",
            "text": "Meta One subscription and Meta Verified discussion",
            "published_at": "2026-09-19",
            "source_url": "https://www.reddit.com/r/InstagramDisabledBans/",
            "collection_method": "Verified public Reddit page"
        },

        {
            "platform": "Reddit",
            "source": "WhatsappBusinessAPI",
            "content_type": "post",
            "text": "Feedback on Meta One and Meta Verified for Business?",
            "published_at": "2026-09-15",
            "source_url": "https://www.reddit.com/r/WhatsappBusinessAPI/",
            "collection_method": "Verified public Reddit page"
        },

        {
            "platform": "Reddit",
            "source": "Instagram",
            "content_type": "post",
            "text": "Meta One subscription",
            "published_at": "2026-09-16",
            "source_url": "https://www.reddit.com/r/Instagram/",
            "collection_method": "Verified public Reddit page"
        },
    ]

    df = pd.DataFrame(reddit_records)

    df["published_at"] = pd.to_datetime(
        df["published_at"],
        utc=True
    )

    df.to_csv(
        REDDIT_OUTPUT,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Verified Reddit records: {len(df)}")
    print(f"Saved to: {REDDIT_OUTPUT}")

    return df


# ============================================================
# UNIFIED DATASET
# ============================================================

def build_unified_dataset(news_df, reddit_df):

    print("\n" + "=" * 60)
    print("BUILDING UNIFIED DATASET")
    print("=" * 60)

    unified_records = []

    # --------------------------------------------------------
    # NEWS
    # --------------------------------------------------------

    if not news_df.empty:

        for _, row in news_df.iterrows():

            text = (
                f"{row['title']}. "
                f"{row['summary']}"
            ).strip()

            unified_records.append({

                "record_id": make_record_id(
                    "News",
                    row["title"],
                    row["published_at_utc"]
                ),

                "platform": "News",

                "source": row["source"],

                "content_type": "article",

                "text": text,

                "published_at": row[
                    "published_at_utc"
                ],

                "engagement_score": None,

                "source_url": row["link"],

                "collection_method":
                    "Google News RSS"

            })

    # --------------------------------------------------------
    # REDDIT
    # --------------------------------------------------------

    if not reddit_df.empty:

        for _, row in reddit_df.iterrows():

            unified_records.append({

                "record_id": make_record_id(
                    "Reddit",
                    row["text"],
                    row["published_at"]
                ),

                "platform": "Reddit",

                "source": row["source"],

                "content_type":
                    row["content_type"],

                "text": row["text"],

                "published_at":
                    row["published_at"],

                "engagement_score": None,

                "source_url":
                    row["source_url"],

                "collection_method":
                    row["collection_method"]

            })

    unified_df = pd.DataFrame(
        unified_records
    )

    if unified_df.empty:
        print("No unified records created.")
        return unified_df

    unified_df = unified_df.drop_duplicates(
        subset=["record_id"]
    )

    unified_df = unified_df.sort_values(
        "published_at"
    ).reset_index(drop=True)

    unified_df.to_csv(
        UNIFIED_OUTPUT,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nUnified dataset created.")
    print(f"Total records: {len(unified_df)}")
    print(
        unified_df["platform"]
        .value_counts()
        .to_string()
    )

    print(f"\nSaved to: {UNIFIED_OUTPUT}")

    return unified_df


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("DATA VORTEX A'26 - ROUND 3")
    print("DATA COLLECTION PIPELINE")
    print("=" * 60)

    print("\nTeam: JOY")
    print(
        "Topic: Public Reaction to a New Pricing "
        "or Subscription Model"
    )
    print("Case Study: Meta One Subscription Model")
    print(
        "Period: 15 September 2026 - "
        "20 September 2026"
    )

    # 1. Collect news
    news_df = collect_google_news()

    # 2. Load verified Reddit records
    reddit_df = load_verified_reddit_data()

    # 3. Build unified dataset
    unified_df = build_unified_dataset(
        news_df,
        reddit_df
    )

    print("\n" + "=" * 60)
    print("COLLECTION PIPELINE COMPLETED")
    print("=" * 60)

    if not unified_df.empty:

        print(
            f"\nFinal records: "
            f"{len(unified_df)}"
        )

        print("\nOutput files:")

        print(
            f"1. {NEWS_OUTPUT}"
        )

        print(
            f"2. {REDDIT_OUTPUT}"
        )

        print(
            f"3. {UNIFIED_OUTPUT}"
        )

    print("\n")


if __name__ == "__main__":
    main()
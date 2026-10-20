import feedparser
import pandas as pd
from datetime import datetime, timezone
from urllib.parse import quote_plus
from pathlib import Path
import re


# ============================================================
# ROUND 3 — META ONE PUBLIC REACTION DATA COLLECTOR
# Source: Google News RSS
# ============================================================

OUTPUT_FILE = Path("data/raw/meta_one_news_raw.csv")

# Recently published window
START_DATE = datetime(2026, 9, 15, tzinfo=timezone.utc)
END_DATE = datetime.now(timezone.utc)

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

# Terms indicating that the article is relevant
RELEVANT_TERMS = [
    "meta one",
    "pricing",
    "price",
    "subscription",
    "cost",
    "monthly",
    "premium",
    "core",
    "paid",
    "pay",
    "worth",
    "expensive",
    "fee",
    "reaction",
    "users",
    "complaint",
    "review",
]

# Unrelated Meta products/topics to exclude
EXCLUDE_TERMS = [
    "meta quest",
    "quest 2",
    "quest 3",
    "quest 3s",
    "vr headset",
    "virtual reality headset",
    "ray-ban",
    "ray ban",
    "smart glasses",
    "smart-glasses",
    "wayfarer",
    "viture",
]


def clean_text(text):
    """Remove HTML and normalize whitespace."""
    text = re.sub(r"<[^>]+>", " ", str(text))
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_relevant(title, summary):
    """Check whether the article is relevant to Meta One pricing/subscription."""

    combined = f"{title} {summary}".lower()

    # Meta One must be explicitly mentioned
    if "meta one" not in combined:
        return False

    # Remove unrelated Meta products
    if any(term in combined for term in EXCLUDE_TERMS):
        return False

    # Must contain at least one relevant pricing/reaction concept
    return any(term in combined for term in RELEVANT_TERMS)


def parse_date(entry):
    """Convert RSS publication date to UTC datetime."""

    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return dt

    return None


def collect():
    records = []

    print("=" * 70)
    print("ROUND 3 — META ONE NEWS COLLECTION")
    print("=" * 70)
    print(f"Start date : {START_DATE.isoformat()}")
    print(f"End date   : {END_DATE.isoformat()}")
    print()

    for query in SEARCH_QUERIES:

        encoded_query = quote_plus(query)

        rss_url = (
            f"https://news.google.com/rss/search?"
            f"q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        )

        print(f"Searching: {query}")

        try:
            feed = feedparser.parse(rss_url)

            candidate_count = 0
            relevant_count = 0

            for entry in feed.entries:

                published_at = parse_date(entry)

                if published_at is None:
                    continue

                candidate_count += 1

                # Keep only recently published data
                if published_at < START_DATE or published_at > END_DATE:
                    continue

                title = clean_text(entry.get("title", ""))
                summary = clean_text(entry.get("summary", ""))
                link = entry.get("link", "")

                if not is_relevant(title, summary):
                    continue

                source_name = ""

                if hasattr(entry, "source"):
                    source_name = entry.source.get("title", "")

                records.append({
                    "published_at_utc": published_at.isoformat(),
                    "title": title,
                    "summary": summary,
                    "source": source_name,
                    "link": link,
                    "query_used": query
                })

                relevant_count += 1

            print(
                f"  Candidates: {candidate_count} | "
                f"Relevant: {relevant_count}"
            )

        except Exception as e:
            print(f"  ERROR: {e}")

    # --------------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------------

    df = pd.DataFrame(records)

    if df.empty:
        print()
        print("NO RELEVANT RECORDS FOUND.")
        return

    # Remove exact duplicate links
    df = df.drop_duplicates(subset=["link"])

    # Remove duplicate title + source combinations
    df = df.drop_duplicates(
        subset=["title", "source"],
        keep="first"
    )

    # Sort newest first
    df["published_at_utc"] = pd.to_datetime(
        df["published_at_utc"],
        utc=True
    )

    df = df.sort_values(
        "published_at_utc",
        ascending=False
    )

    # Collection timestamp
    df.insert(
        0,
        "collected_at_utc",
        datetime.now(timezone.utc).isoformat()
    )

    # Create output directory
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print("=" * 70)
    print("COLLECTION COMPLETE")
    print("=" * 70)
    print(f"Total relevant records : {len(df)}")
    print(f"Saved to               : {OUTPUT_FILE}")
    print()
    print("Sources:")
    print(df["source"].value_counts().to_string())
    print()
    print("Date range:")
    print(
        df["published_at_utc"].min(),
        "to",
        df["published_at_utc"].max()
    )


if __name__ == "__main__":
    collect()
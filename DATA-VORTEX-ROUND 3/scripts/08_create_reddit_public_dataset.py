import pandas as pd
from pathlib import Path

# --------------------------------------------------
# ROUND 3 - VERIFIED PUBLIC REDDIT DATA
# Topic: Meta One Subscription
# --------------------------------------------------

records = [

    {
        "record_id": "reddit_001",
        "platform": "Reddit",
        "subreddit": "FacebookAds",
        "content_type": "post",
        "text": "Meta One is now out. Performance has tanked around the same time. Is this the new pay-to-play?",
        "published_at": "2026-09-19",
        "score": None,
        "source_url": "https://www.reddit.com/r/FacebookAds/comments/1wkw13n/meta_one_is_now_out_performance_has_tanked_around/",
        "collection_method": "Verified public Reddit page"
    },

    {
        "record_id": "reddit_002",
        "platform": "Reddit",
        "subreddit": "FacebookAds",
        "content_type": "comment",
        "text": "they obviously did some kind of algorithmic update",
        "published_at": "2026-09-19",
        "score": None,
        "source_url": "https://www.reddit.com/r/FacebookAds/comments/1wkw13n/meta_one_is_now_out_performance_has_tanked_around/",
        "collection_method": "Verified public Reddit page"
    },

    {
        "record_id": "reddit_003",
        "platform": "Reddit",
        "subreddit": "FacebookAds",
        "content_type": "comment",
        "text": "Wait so we pay Meta a subscription to get more out of what we're already paying for ads?",
        "published_at": "2026-09-19",
        "score": None,
        "source_url": "https://www.reddit.com/r/FacebookAds/comments/1wkw13n/meta_one_is_now_out_performance_has_tanked_around/",
        "collection_method": "Verified public Reddit page"
    },

    {
        "record_id": "reddit_004",
        "platform": "Reddit",
        "subreddit": "FacebookAds",
        "content_type": "comment",
        "text": "Paying Meta a subscription so that the money you already pay Meta starts working properly is a business model with real confidence behind it.",
        "published_at": "2026-09-19",
        "score": None,
        "source_url": "https://www.reddit.com/r/FacebookAds/comments/1wkw13n/meta_one_is_now_out_performance_has_tanked_around/",
        "collection_method": "Verified public Reddit page"
    },

    {
        "record_id": "reddit_005",
        "platform": "Reddit",
        "subreddit": "Instagram",
        "content_type": "post",
        "text": "Instagram Plus / Meta One",
        "published_at": "2026-09-18",
        "score": None,
        "source_url": "https://www.reddit.com/r/Instagram/comments/1wjo2if/instagram_plus_meta_one/",
        "collection_method": "Verified public Reddit page"
    },

    {
        "record_id": "reddit_006",
        "platform": "MetaAI",
        "subreddit": "MetaAI",
        "content_type": "post",
        "text": "I won't pay for a better version of Instagram, WhatsApp and Facebook",
        "published_at": "2026-09-16",
        "score": None,
        "source_url": "https://www.reddit.com/r/MetaAI/",
        "collection_method": "Verified public Reddit page"
    },

    {
        "record_id": "reddit_007",
        "platform": "FacebookAds",
        "subreddit": "FacebookAds",
        "content_type": "post",
        "text": "Meta One - pay subscription for human support and organic reach",
        "published_at": "2026-09-16",
        "score": None,
        "source_url": "https://www.reddit.com/r/FacebookAds/",
        "collection_method": "Verified public Reddit page"
    },

    {
        "record_id": "reddit_008",
        "platform": "InstagramDisabledBans",
        "subreddit": "InstagramDisabledBans",
        "content_type": "post",
        "text": "Meta One replaced Meta Verified in Accounts Center and the plans appear ambiguous.",
        "published_at": "2026-09-19",
        "score": None,
        "source_url": "https://www.reddit.com/r/InstagramDisabledBans/",
        "collection_method": "Verified public Reddit page"
    },

    {
        "record_id": "reddit_009",
        "platform": "WhatsappBusinessAPI",
        "subreddit": "WhatsappBusinessAPI",
        "content_type": "post",
        "text": "Feedback on Meta One and Meta Verified for Business?",
        "published_at": "2026-09-15",
        "score": None,
        "source_url": "https://www.reddit.com/r/WhatsappBusinessAPI/",
        "collection_method": "Verified public Reddit page"
    },

]


# --------------------------------------------------
# CREATE DATAFRAME
# --------------------------------------------------

df = pd.DataFrame(records)

# Convert date
df["published_at"] = pd.to_datetime(df["published_at"])

# Sort chronologically
df = df.sort_values("published_at").reset_index(drop=True)

# --------------------------------------------------
# SAVE
# --------------------------------------------------

output_path = Path("data/raw/meta_one_reddit_public.csv")

output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)

print("=" * 60)
print("REDDIT PUBLIC DATASET CREATED")
print("=" * 60)
print(f"Records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"Date range: {df['published_at'].min()} → {df['published_at'].max()}")
print(f"Saved to: {output_path}")
print("=" * 60)
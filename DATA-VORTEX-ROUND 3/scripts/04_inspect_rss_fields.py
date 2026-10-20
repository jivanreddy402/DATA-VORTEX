import feedparser
from urllib.parse import quote_plus

query = '"Meta One"'

rss_url = (
    "https://news.google.com/rss/search?"
    f"q={quote_plus(query)}&hl=en-US&gl=US&ceid=US:en"
)

feed = feedparser.parse(rss_url)

print("=" * 70)
print("RSS FIELD INSPECTION")
print("=" * 70)

print("Entries found:", len(feed.entries))

if feed.entries:
    entry = feed.entries[0]

    print("\nAVAILABLE FIELDS:")
    for key in entry.keys():
        print("-", key)

    print("\n" + "=" * 70)
    print("FIRST ENTRY")
    print("=" * 70)

    for key, value in entry.items():
        print(f"\n[{key}]")
        print(value)
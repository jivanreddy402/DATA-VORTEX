import requests
import feedparser
from urllib.parse import quote_plus

print("=" * 70)
print("ROUND 3 — REDDIT RSS TEST")
print("=" * 70)

queries = [
    "Meta One",
    '"Meta One"',
    "Meta One subscription",
    "Meta One pricing"
]

headers = {
    "User-Agent": "DATA-VORTEX-ROUND3/1.0 research collector"
}

for query in queries:

    print("\n" + "-" * 70)
    print("QUERY:", query)
    print("-" * 70)

    url = (
        "https://www.reddit.com/search.rss"
        f"?q={quote_plus(query)}"
        "&sort=new"
        "&t=month"
    )

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("STATUS:", response.status_code)
        print("CONTENT TYPE:", response.headers.get("content-type"))

        if response.status_code != 200:
            print("FAILED")
            continue

        feed = feedparser.parse(response.content)

        print("ENTRIES:", len(feed.entries))

        for entry in feed.entries[:3]:

            print("\nTITLE:")
            print(entry.get("title", ""))

            print("\nPUBLISHED:")
            print(entry.get("published", ""))

            print("\nLINK:")
            print(entry.get("link", ""))

            print("\nSUMMARY:")
            print(
                entry.get("summary", "")[:500]
            )

    except Exception as e:
        print("ERROR:", e)

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
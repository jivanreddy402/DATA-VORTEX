import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

FILE = "data/raw/meta_one_news_raw.csv"

df = pd.read_csv(FILE)

print("=" * 70)
print("ROUND 3 — GOOGLE NEWS ARTICLE RESOLUTION TEST")
print("=" * 70)

session = requests.Session()

session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0 Safari/537.36"
    )
})

for i, row in df.head(10).iterrows():

    google_url = row["link"]

    print("\n" + "-" * 70)
    print(f"TEST {i + 1}")
    print("TITLE:", row["title"])
    print("SOURCE:", row["source"])
    print("GOOGLE URL:", google_url)

    try:
        response = session.get(
            google_url,
            timeout=15,
            allow_redirects=True
        )

        print("STATUS:", response.status_code)
        print("FINAL URL:", response.url)

        parsed = urlparse(response.url)

        print("FINAL DOMAIN:", parsed.netloc)

        soup = BeautifulSoup(response.text, "html.parser")

        page_title = soup.title.get_text(
            strip=True
        ) if soup.title else ""

        print("PAGE TITLE:", page_title[:300])

    except Exception as e:
        print("ERROR:", e)

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from pathlib import Path
import re

FILE = "data/raw/meta_one_news_raw.csv"

df = pd.read_csv(FILE)

session = requests.Session()

session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0 Safari/537.36"
    )
})


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_article_text(url):
    try:
        response = session.get(
            url,
            timeout=15,
            allow_redirects=True
        )

        if response.status_code != 200:
            return "", response.status_code, response.url

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup([
            "script",
            "style",
            "nav",
            "header",
            "footer",
            "aside",
            "form"
        ]):
            tag.decompose()

        paragraphs = []

        for p in soup.find_all("p"):
            text = clean_text(p.get_text(" ", strip=True))

            if len(text) >= 40:
                paragraphs.append(text)

        article_text = " ".join(paragraphs)

        return article_text, response.status_code, response.url

    except Exception as e:
        return f"ERROR: {e}", 0, url


print("=" * 70)
print("ROUND 3 — PUBLISHER EXTRACTION TEST")
print("=" * 70)

# Test first 3 records
for i, row in df.head(3).iterrows():

    print("\n" + "-" * 70)
    print(f"TEST {i + 1}")
    print("-" * 70)

    title = row["title"]
    source = row["source"]

    print("TITLE:", title)
    print("SOURCE:", source)

    # Search Google for exact title + source
    search_query = quote_plus(
        f'"{title}" {source}'
    )

    search_url = (
        "https://www.google.com/search?q="
        + search_query
    )

    print("\nSearching publisher article...")

    try:
        response = session.get(
            search_url,
            timeout=15
        )

        print("SEARCH STATUS:", response.status_code)

        soup = BeautifulSoup(response.text, "html.parser")

        links = []

        for a in soup.find_all("a"):
            href = a.get("href", "")

            if href.startswith("http"):
                links.append(href)

        # Remove Google URLs
        links = [
            x for x in links
            if "google.com" not in x
        ]

        if not links:
            print("NO EXTERNAL RESULT FOUND")
            continue

        article_url = links[0]

        print("CANDIDATE URL:")
        print(article_url)

        text, status, final_url = extract_article_text(
            article_url
        )

        print("\nARTICLE STATUS:", status)
        print("FINAL URL:", final_url)
        print("EXTRACTED WORDS:", len(text.split()))

        print("\nARTICLE TEXT PREVIEW:")
        print(text[:1500])

    except Exception as e:
        print("ERROR:", e)

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
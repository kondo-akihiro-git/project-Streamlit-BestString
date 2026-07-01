# strand/yonex/scraper.py
import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

YONEX_STRAND_URL = os.getenv("YONEX_STRAND_URL")
YONEX_BASE_URL = os.getenv("YONEX_BASE_URL")
LIMIT = 12

def fetch_html(offset: int = 0):
    url = f"{YONEX_STRAND_URL}&offset={offset}&limit={LIMIT}"
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def is_roll(name: str) -> bool:
    return re.search(r"[（(]200[mM][)）]$", name) is not None


def parse(html):
    soup = BeautifulSoup(html, "html.parser")

    results = []

    for item in soup.select("li.products-item"):

        title = item.select_one(".products-box__title")
        media = item.select_one("a.products-box__media")
        image = media.select_one("img") if media else None

        if not title or not media:
            continue

        href = media.get("href", "")

        # ストリングマシン(PDF)は除外
        if href.endswith(".pdf"):
            continue

        name = title.get_text(strip=True)

        # ロールガットは除外
        if is_roll(name):
            continue

        results.append({
            "name": name,
            "image_url": (
                f"{YONEX_BASE_URL}{image['src']}"
                if image and image.get("src")
                else None
            ),
        })

    return results


def fetch_all():
    offset = 0
    all_data = []

    while True:
        html = fetch_html(offset)
        data = parse(html)

        if not data:
            break

        all_data.extend(data)
        offset += LIMIT

    return all_data


if __name__ == "__main__":
    data = fetch_all()
    for d in data:
        print(d)
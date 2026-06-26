# racket/scraper.py
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv("YONEX_URL")
LIMIT = 12

def fetch_html(offset: int = 0):
    url = f"{BASE_URL}&offset={offset}&limit={LIMIT}"
    res = requests.get(url)
    res.raise_for_status()
    return res.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("li.products-item")
    results = []
    for item in items:
        name = item.select_one(".products-box__title")
        code = item.select_one(".products-box__number dd")
        results.append({
            "name": name.text.strip() if name else None,
            "code": code.text.strip() if code else None,
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
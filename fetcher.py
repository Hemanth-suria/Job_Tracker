"""
fetcher.py — Pulls live job postings from the Remotive API (free, no API key needed).
https://remotive.com/api-documentation
"""
import requests
from html import unescape
import re

API_URL = "https://remotive.com/api/remote-jobs"


def strip_html(raw: str) -> str:
    """Job descriptions come back as HTML — strip tags for clean storage/search."""
    if not raw:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()[:2000]  # cap length


def fetch_remote_jobs(search: str = "", category: str = "") -> list[dict]:
    """
    Fetch jobs matching a search term and/or category.
    Categories include: software-dev, data, product, marketing, sales, customer-service, etc.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }
    resp = requests.get(API_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    jobs = []
    for j in data.get("jobs", []):
        jobs.append({
            "id": str(j["id"]),
            "title": j.get("title", ""),
            "company": j.get("company_name", ""),
            "location": j.get("candidate_required_location", ""),
            "category": j.get("category", ""),
            "url": j.get("url", ""),
            "published_at": j.get("publication_date", ""),
            "description": strip_html(j.get("description", "")),
        })
    return jobs


if __name__ == "__main__":
    # Quick manual test: python fetcher.py
    results = fetch_remote_jobs(search="python")
    print(f"Fetched {len(results)} jobs")
    for r in results[:3]:
        print(f"- {r['title']} @ {r['company']} ({r['location']})")

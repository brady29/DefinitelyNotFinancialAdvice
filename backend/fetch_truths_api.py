#!/usr/bin/env python3
"""
fetch_truths_api.py
-------------------

• On‑demand fetcher for Truth Social posts
• Handles *both* regular posts and ReTruths
• Usable as   `python backend/fetch_truths_api.py realDonaldTrump -n 5`
"""

import os, json, argparse
from itertools import islice
from bs4 import BeautifulSoup
from truthbrush.api import Api

# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #

def strip_html(html: str) -> str:
    """Convert Truth Social rich‑text HTML into plain text."""
    return BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)

import re 
RT_LINK = re.compile(r'^RT:\s+(https://truthsocial\.com/[^\s]+)')

def normalize(post: dict) -> dict:
    # -------- Case 1: JSON has an actual reblog object --------------------
    if post.get("reblog"):
        orig = post["reblog"]
        return {
            "id": post["id"],
            "created_at": post["created_at"],
            "text": strip_html(orig["content"]) or "[image‑only post]",
            "likes": post["favourites_count"],
            "url": post["url"],
            "is_retruth": True,
            "orig_author": orig["account"]["acct"],
            "orig_url": orig["url"],
        }

    # -------- Case 2: Old‑style “RT: <link>” caption -----------------------
    m = RT_LINK.match(strip_html(post["content"]))
    if m:
        link = m.group(1)
        # author handle is the bit after https://truthsocial.com/@<name>/
        author_match = re.search(r'/@([^/]+)/', link)
        return {
            "id": post["id"],
            "created_at": post["created_at"],
            "text": f"[ReTruth] → {link}",
            "likes": post["favourites_count"],
            "url": post["url"],
            "is_retruth": True,
            "orig_author": author_match.group(1) if author_match else None,
            "orig_url": link,
        }

    # -------- Regular post -------------------------------------------------
    return {
        "id": post["id"],
        "created_at": post["created_at"],
        "text": strip_html(post["content"]) or "[image‑only post]",
        "likes": post["favourites_count"],
        "url": post["url"],
        "is_retruth": False,
        "orig_author": None,
        "orig_url": None,
    }

# --------------------------------------------------------------------------- #
# main fetcher
# --------------------------------------------------------------------------- #

def fetch_truths(handle: str = "realDonaldTrump",
                 n_posts: int | None = 5) -> list[dict]:
    """
    Get `n_posts` newest Truths (`None` → full timeline, beware rate‑limit).

    Returns a list of *normalized* dicts (see normalize() above).
    """
    api = Api()    # auto‑login via TRUTHSOCIAL_USERNAME/PASSWORD

    timeline = api.pull_statuses(username=handle, replies=False, verbose=False)
    gen = timeline if n_posts is None else islice(timeline, n_posts)

    rows = [normalize(st) for st in gen]
    return rows

# --------------------------------------------------------------------------- #
# CLI wrapper so you can run this file directly
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(description="Fetch Truth Social posts.")
    parser.add_argument("handle", nargs="?", default="realDonaldTrump")
    parser.add_argument("-n", "--num", type=int, default=5,
                        help="How many posts (0 or omit for ALL)")
    parser.add_argument("--csv", metavar="FILE",
                        help="Save to CSV instead of printing JSON")
    args = parser.parse_args()

    if not (os.getenv("TRUTHSOCIAL_USERNAME") and os.getenv("TRUTHSOCIAL_PASSWORD")):
        parser.error("Export TRUTHSOCIAL_USERNAME and TRUTHSOCIAL_PASSWORD first.")

    posts = fetch_truths(args.handle,
                         n_posts=None if args.num == 0 else args.num)

    if args.csv:
        import pandas as pd
        pd.DataFrame(posts).to_csv(args.csv, index=False)
        print(f"Saved {len(posts)} posts → {args.csv}")
    else:
        print(json.dumps(posts, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

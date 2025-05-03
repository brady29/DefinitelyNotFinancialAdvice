#!/usr/bin/env python3
"""
fetch_truths_api.py  –  Fetch the latest Truth Social posts via Truthbrush Api.

Requires:
    pip install --no-binary :all: git+https://github.com/stanfordio/truthbrush.git
    pip install beautifulsoup4 python-dotenv pandas



Environment:
    TRUTHSOCIAL_USERNAME  Truth Social login
    TRUTHSOCIAL_PASSWORD  Truth Social password


Set your Truth Social login (once per shell):
    export TRUTHSOCIAL_USERNAME="my_username"
    export TRUTHSOCIAL_PASSWORD="my_password"
"""

import os
import argparse   # easy command‑line parsing
import json
from itertools import islice  # lets us take the first N items from a generator

from bs4 import BeautifulSoup  # strip HTML tags
from truthbrush.api import Api  # main Truthbrush entry‑point


def strip_html(html: str) -> str:
    """Convert the rich‑text HTML in a Truth post into plain text."""
    return BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)


def fetch_truths(handle="realDonaldTrump", n_posts: int | None = 5):
    """
    Return a list of Truths.
      • n_posts = None  → return ALL posts
      • n_posts = 10    → return newest 10 posts
    """
    api = Api()
    timeline = api.pull_statuses(username=handle, replies=False, verbose=False)

    rows = []
    generator = timeline if n_posts is None else islice(timeline, n_posts)

    for st in generator:
        rows.append(
            {
                "created_at": st["created_at"],
                "id": st["id"],
                "text": strip_html(st["content"]) or "[image‑only post]",
                "likes": st["favourites_count"],
                "url": st["url"],
            }
        )
    return rows


def main():
    """CLI wrapper so you can run:  python truth_fetcher.py realDonaldTrump -n 5"""
    parser = argparse.ArgumentParser(description="Fetch latest Truth Social posts.")
    parser.add_argument("handle", nargs="?", default="realDonaldTrump",
                        help="Username (no @). Default = realDonaldTrump")
    parser.add_argument("-n", "--num", type=int, default=5,
                        help="How many posts to fetch (default 5)")
    parser.add_argument("--csv", metavar="FILE",
                        help="Save result to CSV instead of printing JSON")
    args = parser.parse_args()

    # Quick check: did the user set their Truth Social creds?
    if not (os.getenv("TRUTHSOCIAL_USERNAME") and os.getenv("TRUTHSOCIAL_PASSWORD")):
        parser.error("Please export TRUTHSOCIAL_USERNAME and TRUTHSOCIAL_PASSWORD first.")

    # Fetch posts
    posts = fetch_truths(args.handle, args.num)

    # Either print JSON to the terminal...
    if not args.csv:
        print(json.dumps(posts, indent=2, ensure_ascii=False))
    # ...or save to a CSV file.
    else:
        import pandas as pd
        pd.DataFrame(posts).to_csv(args.csv, index=False)
        print(f"Saved {len(posts)} posts to {args.csv}")


# Only run main() if the file is executed directly, not when imported
if __name__ == "__main__":
    main()
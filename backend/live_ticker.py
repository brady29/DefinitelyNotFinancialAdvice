#!/usr/bin/env python3
"""
live_ticker.py  –  Trump account

Appends any brand‑new posts from @realDonaldTrump
to trump_truths_all.jsonl every POLL_SECONDS, skipping duplicates.
"""

import json
import time
import pathlib
from itertools import islice
from truthbrush.api import Api
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

ACCOUNT      = "realDonaldTrump"
OUTFILE      = pathlib.Path("trump_truths_all.jsonl")
POLL_SECONDS = 60      # how often to poll
SEED_POSTS   = 40      # how many to grab on first run
BACKOFF_SECS = 600     # wait 10 min if rate‑limited

def strip_html(h: str) -> str:
    return BeautifulSoup(h or "", "html.parser").get_text(" ", strip=True)

def tail_last_id(path: pathlib.Path) -> str | None:
    """Return the ID of the newest post already in the archive, or None."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return None
    return json.loads(lines[-1])["id"]

def main():
    api = Api()
    OUTFILE.touch(exist_ok=True)

    last_seen = tail_last_id(OUTFILE)

    # first‐run seed
    if last_seen is None:
        print("[ticker] Empty archive – seeding initial posts")
        seed = list(islice(api.pull_statuses(username=ACCOUNT, replies=False), SEED_POSTS))
        with OUTFILE.open("a", encoding="utf-8") as fp:
            for post in reversed(seed):
                fp.write(json.dumps({
                    "id":          post["id"],
                    "created_at":  post["created_at"],
                    "text":        strip_html(post["content"]),
                    "likes":       post["favourites_count"],
                    "url":         post["url"],
                }, ensure_ascii=False) + "\n")
        last_seen = seed[0]["id"]
        print("[ticker] Seed complete.")

    while True:
        new_items = []
        try:
            for st in api.pull_statuses(username=ACCOUNT, replies=False, verbose=False):
                if st["id"] == last_seen:
                    break
                new_items.append({
                    "id":          st["id"],
                    "created_at":  st["created_at"],
                    "text":        strip_html(st["content"]),
                    "likes":       st["favourites_count"],
                    "url":         st["url"],
                })
        except HTTPError as e:
            print(f"[ticker] Rate‑limited; sleeping {BACKOFF_SECS}s")
            time.sleep(BACKOFF_SECS)
            continue

        if new_items:
            # write oldest→newest so file stays chronological
            with OUTFILE.open("a", encoding="utf-8") as fp:
                for rec in reversed(new_items):
                    fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
            # **CRITICAL**: update last_seen so we don’t re‐append next time
            last_seen = new_items[0]["id"]
            print(f"[ticker] Added {len(new_items)} new post(s).")

        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()
    
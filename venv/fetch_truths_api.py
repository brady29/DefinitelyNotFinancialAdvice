#!/usr/bin/env python
from bs4 import BeautifulSoup
from truthbrush.api import Api

def strip_html(html: str) -> str:
    return BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)

def latest_truths(handle="realDonaldTrump", n=5):
    api = Api()                                           # auto‑auth via env vars
    timeline = api.pull_statuses(username=handle, replies=False, verbose=False)

    rows = []
    for st in timeline:                                   # generator
        rows.append(
            {
                "created_at": st["created_at"],
                "id": st["id"],
                "text": strip_html(st["content"]) or "[image‑only post]",
                "likes": st["favourites_count"],
                "url": st["url"],
            }
        )
        if len(rows) >= n:                                # stop after n posts
            break
    return rows

if __name__ == "__main__":
    for post in latest_truths(n=5):
        print(f"{post['created_at'][:19]}  {post['text'][:100]}")
        print(" ↳", post["url"], "\n")

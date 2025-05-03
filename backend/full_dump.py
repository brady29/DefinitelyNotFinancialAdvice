# full_dump.py  – run once to back‑fill all Trump Truths

import json, time
from truthbrush.api import Api
from bs4 import BeautifulSoup
from pathlib import Path

OUTFILE = Path("trump_truths_all.jsonl")      # one JSON per line
ACCOUNT  = "realDonaldTrump"

def strip_html(html: str) -> str:
    return BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)

def main():
    api   = Api()                       # env creds
    count = 0
    # pull_statuses yields newest→oldest until it exhausts the timeline
    for st in api.pull_statuses(username=ACCOUNT, replies=False, verbose=True):
        record = {
            "id"        : st["id"],
            "created_at": st["created_at"],
            "text"      : strip_html(st["content"]),
            "likes"     : st["favourites_count"],
            "url"       : st["url"],
        }
        OUTFILE.write_text("", encoding="utf‑8")  # create empty file
        with OUTFILE.open("a", encoding="utf‑8") as fp:
            fp.write(json.dumps(record, ensure_ascii=False) + "\n")
        count += 1
        # 🚦 courtesy delay so we don't hammer Truth Social
        if count % 500 == 0:
            time.sleep(2)

    print(f"Saved {count} total posts → {OUTFILE}")

if __name__ == "__main__":
    main()

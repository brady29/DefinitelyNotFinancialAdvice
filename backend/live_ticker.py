# live_ticker.py  – run as a background process / cron job

import json, time, pathlib
from itertools import islice
from truthbrush.api import Api
from bs4 import BeautifulSoup

ACCOUNT   = "realDonaldTrump"
OUTFILE   = pathlib.Path("trump_truths_all.jsonl")
POLL_SECS = 60                              # check every 60 s

def strip_html(h):
    from bs4 import BeautifulSoup
    return BeautifulSoup(h or "", "html.parser").get_text(" ", strip=True)

def tail_last_id(path):
    """Return the id of the newest post in the JSONL file."""
    *_, last = path.read_text(encoding="utf‑8").splitlines()
    return json.loads(last)["id"]

def main():
    api = Api()
    last_id = tail_last_id(OUTFILE)

    while True:
        # Generator yields newest→oldest; stop when we hit last_id
        new_items = []
        for st in api.pull_statuses(username=ACCOUNT, replies=False, verbose=False):
            if st["id"] == last_id:
                break
            new_items.append({
                "id": st["id"],
                "created_at": st["created_at"],
                "text": strip_html(st["content"]),
                "likes": st["favourites_count"],
                "url": st["url"],
            })
        if new_items:
            # Append in reverse so chronological order is preserved in file
            with OUTFILE.open("a", encoding="utf‑8") as fp:
                for rec in reversed(new_items):
                    fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
            last_id = new_items[0]["id"]
            print(f"Added {len(new_items)} new posts.")

        time.sleep(POLL_SECS)

if __name__ == "__main__":
    main()
    
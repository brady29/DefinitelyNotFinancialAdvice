"""
live_ticker.py: HOW TO USE
============================

Purpose
-------
• Runs forever (or until Ctrl-C)  
• Checks Trump's Truth Social feed once every POLL_SECONDS  
• Saves any brand-new posts to trump_truths_all.jsonl  
  ↳  After first run you have a growing local archive
• Prints a line only when it seeds the file or finds new posts

Quick start
-----------
1.  Activate your virtual env and export Truth Social creds:

        source venv/bin/activate
        export TRUTHSOCIAL_USERNAME=demo_user
        export TRUTHSOCIAL_PASSWORD='demo_pass'

2.  Launch the ticker in its own terminal tab:

        python backend/live_ticker.py

   •  First run: seeds ~40 recent posts, then sleeps/polls.  
   •  Every minute: prints “[ticker] Added X new posts.” if something new.  
   •  The JSONL file grows silently when there's nothing new.

Useful tips
-----------
•  View the file live:   `tail -f trump_truths_all.jsonl`  
•  Keep it running after you close SSH:  
       `nohup python backend/live_ticker.py &> ticker.log &`  
•  Safe to run alongside FastAPI; both use the same creds.
"""

import json, time, pathlib
from itertools import islice
from truthbrush.api import Api
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

ACCOUNT   = "realDonaldTrump"
OUTFILE   = pathlib.Path("trump_truths_all.jsonl")
POLL_SECS = 60                              # check every 60 s
HANDLE        = "realDonaldTrump"            # which account to watch
ARCHIVE_FILE  = pathlib.Path("trump_truths_all.jsonl")
POLL_SECONDS  = 60                           # how often to poll
SEED_POSTS    = 40                           # first‑run seed batch
BACKOFF_SECS  = 600                          # sleep 10 min on rate‑limit


def strip_html(h):
    from bs4 import BeautifulSoup
    return BeautifulSoup(h or "", "html.parser").get_text(" ", strip=True)

def tail_last_id(path):
    """
    Return the ID of the newest post already in the archive.
    If the file is empty, return None.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:           # file is empty
        return None
    return json.loads(lines[-1])["id"]

SEED_POSTS  = 40      # how many to grab on first run (one or two pages)
BACKOFF_SECS = 600    # wait 10 min if Cloudflare says “rate‑limited”

def main():
    api = Api()
      # create the JSONL file if it doesn’t exist yet ✱
    ARCHIVE_FILE.touch(exist_ok=True)

    last_seen = tail_last_id(ARCHIVE_FILE)   # may return None if file is empty


    # if archive is empty, seed first page (≈20 posts)
    if last_seen is None:
        print("[ticker] Empty archive – seeding initial posts")
        seed = list(islice(api.pull_statuses(username=HANDLE, replies=False), 40))
        with ARCHIVE_FILE.open("a", encoding="utf-8") as fp:
            for post in reversed(seed):
                fp.write(json.dumps({
                    "id": post["id"],
                    "created_at": post["created_at"],
                    "text": strip_html(post["content"]),
                    "likes": post["favourites_count"],
                    "url": post["url"],
                }, ensure_ascii=False) + "\n")
        last_seen = seed[0]["id"]
        print("[ticker] Seed complete.")

    while True:
        # Generator yields newest→oldest; stop when we hit last_id
        new_items = []
        for st in api.pull_statuses(username=ACCOUNT, replies=False, verbose=False):
            if st["id"] == last_seen:   
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
    
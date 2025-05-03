#!/usr/bin/env python3
"""
our_live_ticker.py  –  DNFA account

Appends any brand‑new posts from @DefinitelyNotFinancialAdvice
to dnfa_truths.jsonl every 30 seconds.  Skips duplicates.
"""

import json, time, pathlib
from truthbrush.api import Api
from bs4 import BeautifulSoup

ACCOUNT      = "DefinitelyNotFinancialAdvice"
OUTFILE      = pathlib.Path("dnfa_truths.jsonl")
POLL_SECONDS = 30

def strip_html(h):
    return BeautifulSoup(h or "", "html.parser").get_text(" ", strip=True)

# --------------------------------------------------------------------------- #
# NEW: load the set of IDs already saved                                    ###
# --------------------------------------------------------------------------- #
def load_existing_ids(path: pathlib.Path) -> set[str]:
    ids = set()
    if path.exists():
        with path.open("r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if line:
                    ids.add(json.loads(line)["id"])
    return ids
# --------------------------------------------------------------------------- #

def main():
    api = Api()
    OUTFILE.touch(exist_ok=True)
    known_ids = load_existing_ids(OUTFILE)        # ← use the helper
    print(f"[dnfa‑ticker] booted with {len(known_ids)} known IDs")

    while True:
        new_items = []
        for st in api.pull_statuses(username=ACCOUNT, replies=True, verbose=False):
            if st["id"] in known_ids:
                break                    # timeline is newest→oldest; stop at first known
            new_items.append(st)

        if new_items:
            with OUTFILE.open("a", encoding="utf-8") as fp:
                for st in reversed(new_items):     # oldest→newest
                    rec = {
                        "id"        : st["id"],
                        "created_at": st["created_at"],
                        "text"      : strip_html(st["content"]),
                        "url"       : st["url"],
                    }
                    fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    known_ids.add(st["id"])        # update the set
            print(f"[dnfa‑ticker] saved {len(new_items)} new post(s).")

        time.sleep(POLL_SECONDS)

if __name__ == "__main__":
    main()

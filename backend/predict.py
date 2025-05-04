#!/usr/bin/env python3
# backend/predict.py

import argparse
import json
import logging
from backend.fetch_truths_api import fetch_truths
from backend.gemini_client    import genai_predict

# ─── QUIET DOWN TOO‑VERBOSE LOGGERS ──────────────────────────────────────────
logging.getLogger("truthbrush.api").setLevel(logging.WARNING)
logging.getLogger("google_genai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    p = argparse.ArgumentParser(
        description="Fetch recent TruthSocial posts and get a one‑word Gemini prediction + reason."
    )
    p.add_argument("ticker", help="Stock symbol, e.g. AAPL")
    p.add_argument("-n", "--num", type=int, default=5,
                   help="How many TruthSocial posts to fetch")
    args = p.parse_args()

    # 1) Grab the last n posts
    raw = fetch_truths("realDonaldTrump", n_posts=args.num)
    texts = [post["text"] for post in raw]

    # 2) Print which posts we're feeding in
    print("Checking these posts:")
    for i, t in enumerate(texts, 1):
        print(f"{i}. {t}")

    # 3) Get back a (prediction, reason) tuple
    prediction, reason = genai_predict(
        system=(
            "You are a financial‑advisor bot. "
            "Respond **exactly** with one of: UP, DOWN, STAY_FLAT. "
            "Do NOT add any other text. "
            "On the next line, give a one‑sentence reason."
        ),
        user="\n\n".join(texts)
    )

    # 4) Output JSON
    out = {
        "ticker":      args.ticker,
        "posts_used":  texts,
        "prediction":  prediction,
        "reason":      reason
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

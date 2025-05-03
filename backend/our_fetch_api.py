#!/usr/bin/env python3
"""
Quick fetcher for our own Truth Social demo account.
Usage: python backend/fetch_dnfa_api.py -n 5
"""

from .fetch_truths_api import fetch_truths  # reuse your normalizer

def fetch_own(n_posts=5):
    return fetch_truths("DefinitelyNotFinancialAdvice", n_posts)

if __name__ == "__main__":
    import json, argparse
    p = argparse.ArgumentParser()
    p.add_argument("-n", "--num", type=int, default=5)
    args = p.parse_args()
    print(json.dumps(fetch_own(args.num), indent=2, ensure_ascii=False))
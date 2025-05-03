#!/usr/bin/env python3
"""
api_fast.py
===========

FastAPI server that exposes:

    • GET /truth/latest?n=20        → newest Trump Truths
    • GET /dnfa/latest?n=10         → newest posts from our demo account

Run (dev):

    uvicorn backend.api_fast:app --reload
"""

from pathlib import Path
from collections import deque
from typing import List, Dict, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json                      # ← add this line


# Relative imports (dot = same package)
from .fetch_truths_api import fetch_truths
from .our_fetch_api  import fetch_own     # on‑demand for our account

# --------------------------------------------------------------------------- #
# FastAPI setup
# --------------------------------------------------------------------------- #

app = FastAPI(
    title="Truth‑to‑Tick API",
    version="0.2.0",
    description="Serves Truth Social posts for the front‑end demo.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # allow all during dev
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

DNFA_FILE = Path("dnfa_truths.jsonl")      # written by our_live_ticker.py

def tail_jsonl(path: Path, n: int) -> List[Dict]:
    """Return the last *n* lines of a JSONL file as a list of dicts."""
    dq: deque = deque(maxlen=n)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fp:
        for line in fp:
            dq.append(json.loads(line))
    return list(dq)

# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #

@app.get("/truth/latest", response_model=List[Dict])
def latest_truths(
    n: Optional[int] = Query(
        5, gt=0, le=1000,
        description="Number of posts to return (omit for ALL ≈ 26 k)"
    )
):
    """
    Newest Truths from @realDonaldTrump.
    """
    try:
        return fetch_truths(n_posts=n)
    except Exception as err:
        raise HTTPException(status_code=503, detail=str(err))


@app.get("/dnfa/latest", response_model=List[Dict])
def dnfa_latest(
    n: int = Query(5, gt=0, le=50,
                   description="Newest posts from our demo account")
):
    """
    Latest posts from @DefinitelyNotFinancialAdvice.

    • First tries the ticker file (dnfa_truths.jsonl)
    • Falls back to a live API pull if ticker hasn’t run yet
    """
    if DNFA_FILE.exists() and DNFA_FILE.stat().st_size:
        return tail_jsonl(DNFA_FILE, n)
    # fallback live pull (small n so we don’t rate‑limit)
    try:
        return fetch_own(n)
    except Exception as err:
        raise HTTPException(status_code=503, detail=str(err))

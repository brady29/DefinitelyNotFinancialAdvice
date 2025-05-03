# api_fast.py  ------------------------------------------------------------
"""
FastAPI wrapper that exposes a single endpoint:

    GET /truth/latest?n=5    →  JSON array of the n most‑recent Trump Truths

Dependencies (already in requirements.txt):
    fastapi
    uvicorn[standard]
    python-dotenv
    beautifulsoup4
    git+https://github.com/stanfordio/truthbrush.git
"""

from typing import List, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.fetch_truths_api import fetch_truths       # <- your helper function
from portfolio import PortfolioApp  # Import PortfolioApp class

# OPTIONAL: background live ticker
# from threading import Thread
# from live_ticker import main as ticker_main

# --------------------------------------------------------------------------- #
# FastAPI app setup
# --------------------------------------------------------------------------- #

app = FastAPI(
    title="Tweet‑to‑Tick API",
    description="Serves Trump Truth Social posts for the front‑end",
    version="0.1.0",
)

# Allow any origin during dev; lock this down in prod if you like
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------------- #
# (Optional) launch the live_ticker in a background thread
# --------------------------------------------------------------------------- #
# def start_ticker():
#     """Append new posts to trump_truths_all.jsonl every 60 s."""
#     Thread(target=ticker_main, daemon=True).start()
#
# start_ticker()

# --------------------------------------------------------------------------- #
# Routes
# --------------------------------------------------------------------------- #

from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException, Query

@app.get("/truth/latest", response_model=List[Dict])
def latest_truths(
    n: Optional[int] = Query(
        None, gt=0, le=1000,
        description="How many posts (omit for ALL ≈ 26 k posts)"
    )
):
    """
    GET /truth/latest        → returns ALL posts
    GET /truth/latest?n=50   → returns 50 newest posts
    """
    try:
        return fetch_truths(n_posts=n)   # None means fetch all
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

# Create an instance of PortfolioApp
portfolio_app = PortfolioApp()

@app.get("/portfolio/data", response_model=Dict)
def get_portfolio_data():
    """
    GET /portfolio/data  → returns portfolio data as JSON
    """
    try:
        return portfolio_app.get_portfolio_data()
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

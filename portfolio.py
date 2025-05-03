#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Dict, Tuple, Any, List

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd  

matplotlib.use("TkAgg")

TIMEFRAMES: Dict[str, Tuple[str, str]] = {
    "1D": ("1d", "5m"),
    "1W": ("5d", "15m"),
    "1M": ("1mo", "60m"),
    "3M": ("3mo", "1d"),
    "1Y": ("1y", "1d"),
    "5Y": ("5y", "1wk"),
}

_WINDOW_SLICE = {
    "1D": "1D",
    "1W": "7D",
    "1M": "30D",
    "3M": "90D",
    "1Y": "365D",
    "5Y": "1825D",
}

START_CAPITAL = 10_000.0


def _scalar(val: Any):
    """Extract scalar from 1‑element pandas Series/list, else return as‑is."""
    if isinstance(val, pd.Series):
        return val.iloc[0] if len(val) == 1 else val
    if isinstance(val, (list, tuple)) and len(val) == 1:
        return val[0]
    return val


class PortfolioApp(tk.Tk):
    """Tkinter GUI for interactive stock & portfolio visualisation."""

    def __init__(self):
        super().__init__()
        self.title("Definitely Not Financial Advice")
        self.geometry("1100x650")
        self.configure(bg="#f5f5f5")

        # state
        self.portfolio: List[str] = []  # list of tickers
        self.selected_ticker: str | None = None  # None means portfolio view
        self.selected_tf: str = "1D"

        self._build_widgets()

   #Python gui
    def _build_widgets(self):
        left = ttk.Frame(self, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        # entry + add
        self.symbol_var = tk.StringVar()
        entry = ttk.Entry(left, textvariable=self.symbol_var)
        entry.pack(fill=tk.X, pady=(0, 5))
        entry.bind("<Return>", lambda *_: self.add_symbol())
        ttk.Button(left, text="Add Stock", command=self.add_symbol).pack(fill=tk.X)

        # listbox
        self.listbox = tk.Listbox(left, height=18, exportselection=False)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        # action buttons
        actions = ttk.Frame(left)
        actions.pack(fill=tk.X, pady=(0, 6))
        ttk.Button(actions, text="View Portfolio", command=self.show_portfolio).pack(fill=tk.X)
        ttk.Button(actions, text="Sell All", command=self.sell_selected).pack(fill=tk.X, pady=(4, 0))

        # info label
        self.info_var = tk.StringVar(value="Add tickers to build a portfolio…")
        ttk.Label(left, textvariable=self.info_var, wraplength=190).pack(fill=tk.X, pady=5)

        # main chart area
        right = ttk.Frame(self, padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # timeframe bar
        tf_bar = ttk.Frame(right)
        tf_bar.pack(fill=tk.X)
        for tf in TIMEFRAMES:
            ttk.Button(tf_bar, text=tf, command=lambda t=tf: self.change_timeframe(t)).pack(side=tk.LEFT, padx=3)

        # matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 4.8))
        self.ax.set_title("No data yet")
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

    #Handlers
    def add_symbol(self):
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            return
        if symbol in self.portfolio:
            messagebox.showinfo("Duplicate", f"{symbol} already in portfolio.")
            return
        try:
            yf.Ticker(symbol).fast_info  # simple validity check
        except Exception:
            messagebox.showerror("Error", f"Ticker '{symbol}' not found.")
            return
        self.portfolio.append(symbol)
        self.listbox.insert(tk.END, symbol)
        self.symbol_var.set("")
        self.status_var.set(f"Added {symbol}")

    def sell_selected(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Sell All", "Select a ticker to sell.")
            return
        idx = sel[0]
        ticker = self.portfolio.pop(idx)
        self.listbox.delete(idx)
        self.status_var.set(f"Sold all shares of {ticker}")

        # update state
        if ticker == self.selected_ticker:
            self.selected_ticker = None

        # refresh display
        if self.selected_ticker:
            self.plot_current()
        elif self.portfolio:
            self.plot_portfolio()
        else:
            self.clear_chart()
            self.info_var.set("Portfolio is empty.")

    def clear_chart(self):
        self.ax.clear()
        self.ax.set_title("No data")
        self.canvas.draw_idle()

    def _on_select(self, *_):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.selected_ticker = self.portfolio[sel[0]]
        self.plot_current()

    def show_portfolio(self):
        if not self.portfolio:
            messagebox.showinfo("Portfolio", "Add at least one stock first.")
            return
        self.selected_ticker = None
        self.plot_portfolio()

    def change_timeframe(self, tf: str):
        self.selected_tf = tf
        if self.selected_ticker:
            self.plot_current()
        elif self.portfolio:
            self.plot_portfolio()

    #stock chart graphing
    def plot_current(self):
        if not self.selected_ticker:
            return
        period, interval = TIMEFRAMES[self.selected_tf]
        self.status_var.set(f"Fetching {self.selected_ticker} {self.selected_tf}…")
        self.after(50, lambda: self._async_plot_stock(self.selected_ticker, period, interval))

    def _async_plot_stock(self, symbol: str, period: str, interval: str):
        try:
            data = yf.download(symbol, period=period, interval=interval, progress=False, threads=False)
            if data.empty:
                raise ValueError("No data returned")

            self.ax.clear()
            self.ax.plot(data.index, data["Close"], linewidth=1.2)
            self.ax.set_title(f"{symbol} – {self.selected_tf}")
            self.ax.set_xlabel("Date")
            self.ax.set_ylabel("Price ($)")
            self.fig.autofmt_xdate()
            self.canvas.draw_idle()

            # quick price snapshot
            ticker = yf.Ticker(symbol)
            fast = getattr(ticker, "fast_info", {}) or {}
            last_close = _scalar(fast.get("previous_close"))
            current = _scalar(fast.get("last_price")) or _scalar(fast.get("regular_market_price"))
            if last_close is None and len(data) >= 2:
                last_close = data["Close"].iloc[-2]
            if current is None and not data.empty:
                current = data["Close"].iloc[-1]

            if isinstance(last_close, (int, float)) and isinstance(current, (int, float)) and last_close != 0:
                change = (current - last_close) / last_close * 100
                self.info_var.set(f"{symbol}\nLast: ${last_close:.2f}\nNow:  ${current:.2f} ({change:+.2f}%)")
            else:
                self.info_var.set("Price data unavailable.")

            self.status_var.set(f"Updated {symbol} at {datetime.now().strftime('%H:%M:%S')}")

        except Exception as exc:
            messagebox.showerror("Error", f"Failed to fetch data for {symbol}: {exc}")
            self.status_var.set("Error – see dialog")

    #whole portfolio graphing
    def plot_portfolio(self):
        self.status_var.set("Building portfolio value…")
        self.after(50, lambda: self._async_plot_portfolio(self.selected_tf))

    def _async_plot_portfolio(self, tf_key: str):
        try:
            if not self.portfolio:
                raise RuntimeError("No tickers in portfolio")

            # download 5‑year daily closes for all tickers
            data = yf.download(
                self.portfolio,
                period="5y",
                interval="1d",
                group_by="ticker",
                threads=False,
                progress=False,
            )
            if data.empty:
                raise ValueError("No data returned")

            # normalise to a simple DataFrame of close prices per ticker
            if isinstance(data.columns, pd.MultiIndex):
                closes = data.loc[:, pd.IndexSlice[:, "Close"]]
                closes.columns = [c[0] for c in closes.columns]
            else:  # single ticker case
                closes = data[["Close"]].rename(columns={"Close": self.portfolio[0]})

            # determine shares purchased 5y ago with equal allocation
            alloc_per = START_CAPITAL / len(self.portfolio)
            shares: Dict[str, float] = {}
            for t in self.portfolio:
                series = closes[t].dropna()
                if series.empty:
                    raise ValueError(f"No price data for {t}")
                first_price = series.iloc[0]
                shares[t] = alloc_per / first_price

            # aggregate portfolio value over time
            port_val = pd.Series(index=closes.index, dtype=float)
            for t, sh in shares.items():
                port_val = port_val.add(closes[t] * sh, fill_value=0)
            port_val.name = "Portfolio"

            # slice according to timeframe
            window = _WINDOW_SLICE[tf_key]
            sliced = port_val.last(window)
            if sliced.empty:
                sliced = port_val

            # plot
            self.ax.clear()
            self.ax.plot(sliced.index, sliced.values, linewidth=1.6)
            self.ax.set_title(f"Portfolio – {tf_key}")
            self.ax.set_xlabel("Date")
            self.ax.set_ylabel("Value ($)")
            self.fig.autofmt_xdate()
            self.canvas.draw_idle()

            # summary
            current_val = port_val.iloc[-1]
            pct_return = (current_val - START_CAPITAL) / START_CAPITAL * 100
            self.info_var.set(
                f"Current portfolio value: ${current_val:,.2f}\nReturn: {pct_return:+.2f}% since start"
            )
            self.status_var.set(f"Portfolio updated at {datetime.now().strftime('%H:%M:%S')}")

        except Exception as exc:
            messagebox.showerror("Error", f"Portfolio calculation failed: {exc}")
            self.status_var.set("Error – see dialog")

    def get_portfolio_data(self):
        """Fetch portfolio data as a JSON object."""
        portfolio_data = {
            "portfolio": self.portfolio,
            "selected_ticker": self.selected_ticker,
            "selected_tf": self.selected_tf,
        }
        return portfolio_data


if __name__ == "__main__":
    PortfolioApp().mainloop()

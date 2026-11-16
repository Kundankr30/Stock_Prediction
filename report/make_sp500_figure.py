#!/usr/bin/env python3
"""Draw the S&P 500 chart with the train / validation / test regions (Figure 4.2).

Usage (run where Yahoo Finance is reachable, e.g. in your WSL notebook environment):
    python make_sp500_figure.py                    # downloads ^GSPC with yfinance
    python make_sp500_figure.py sp500_features.csv # or use your saved Step 1 file (Date, close)
Writes figures/fig_sp500_split.pdf.  The split is 70/15/15 of the trading days.
"""
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    df = pd.read_csv(sys.argv[1])
    dcol = "Date" if "Date" in df.columns else df.columns[0]
    ccol = next(c for c in df.columns if c.lower() in ("close", "adj close"))
    s = df.set_index(pd.to_datetime(df[dcol]))[ccol].sort_index()
else:
    import yfinance as yf
    raw = yf.download("^GSPC", start="2008-08-01", end="2016-07-02", auto_adjust=True)
    s = raw["Close"].squeeze()

n = len(s); i1, i2 = int(n * 0.70), int(n * 0.85)
t1, t2 = s.index[i1], s.index[i2]
plt.rcParams["font.family"] = "serif"
fig, ax = plt.subplots(figsize=(8, 3.4))
ax.plot(s.index, s.values, color="#1f2a44", lw=1.1)
for a, b, c, lab in [(s.index[0], t1, "#DDF1EE", "Train (70%)"), (t1, t2, "#E8E1F8", "Val (15%)"), (t2, s.index[-1], "#FBE3DF", "Test (15%)")]:
    ax.axvspan(a, b, color=c, alpha=0.8, lw=0)
    ax.text(a + (b - a) / 2, ax.get_ylim()[1] * 0.98, lab, ha="center", va="top", fontsize=9)
ax.set_ylabel("S&P 500 close"); ax.set_xlim(s.index[0], s.index[-1])
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("figures/fig_sp500_split.pdf")
print("saved figures/fig_sp500_split.pdf", s.index[0].date(), t1.date(), t2.date(), s.index[-1].date())

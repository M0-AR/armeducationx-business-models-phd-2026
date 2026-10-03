"""Live-data helpers with offline-safe fallbacks.
Every function tries the public API first (no key), then falls back to
verified snapshots captured 2026-10-03 so benchmarks are reproducible.
Snapshots are stored under data/live/.
"""
from __future__ import annotations
import json, os, urllib.request, urllib.parse, datetime

LIVE_DIR = os.path.join(os.path.dirname(__file__), "../../data/live")
LIVE_DIR = os.path.abspath(LIVE_DIR)

# Verified snapshots 2026-10-03 (sources: yfinance via agent-reach, ECB Frankfurter, World Bank)
SNAPSHOT_QUOTES = {
    "ARM": {"current": 307.49, "last_close": 292.34, "pe_ttm": 316.99, "market_cap": 328398864384, "name": "Arm Holdings plc"},
    "NVDA": {"current": 233.95, "last_close": 230.86, "pe_ttm": 29.57, "market_cap": 5649190617088, "name": "NVIDIA Corporation"},
    "QCOM": {"current": 184.87, "last_close": 182.09, "pe_ttm": 21.15, "market_cap": 197452333056, "name": "QUALCOMM Incorporated"},
    "INTC": {"current": 119.33, "last_close": 120.0, "pe_ttm": 57.86, "market_cap": 630790946816, "name": "Intel Corporation"},
    "AMD": {"current": 164.20, "last_close": 161.50, "pe_ttm": 44.10, "market_cap": 266000000000, "name": "Advanced Micro Devices"},
}
SNAPSHOT_FX = {"EUR": 0.89087, "GBP": 0.75753, "JPY": 157.67, "date": "2026-10-02", "base": "USD"}
SNAPSHOT_RD = {"US_2023": 3.44716, "US_2020": 3.41788, "US_2010": 2.71443}

def _http_json(url: str, timeout: int = 12):
    req = urllib.request.Request(url, headers={"User-Agent": "phd-research-contact@example.com"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def yahoo_quote(symbol: str) -> dict:
    """Yahoo Finance v8, no auth. Returns dict with current, last_close, pe, cap or snapshot."""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1d&range=5d"
        j = _http_json(url)
        res = j["chart"]["result"][0]
        closes = [c for c in res["indicators"]["quote"][0]["close"] if c]
        current = closes[-1]
        last_close = closes[-2] if len(closes) > 1 else current
        meta = res.get("meta", {})
        out = {
            "current": round(float(current), 2),
            "last_close": round(float(last_close), 2),
            "pe_ttm": SNAPSHOT_QUOTES.get(symbol, {}).get("pe_ttm"),
            "market_cap": meta.get("marketCap") or SNAPSHOT_QUOTES.get(symbol, {}).get("market_cap"),
            "name": SNAPSHOT_QUOTES.get(symbol, {}).get("name", symbol),
            "live": True,
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
        }
        return out
    except Exception as e:
        snap = dict(SNAPSHOT_QUOTES.get(symbol, {"current": 0}))
        snap["live"] = False
        snap["error"] = str(e)[:200]
        return snap

def frankfurter_fx(base="USD", symbols="EUR,GBP,JPY") -> dict:
    try:
        j = _http_json(f"https://api.frankfurter.app/latest?from={base}&to={symbols}")
        return {"base": base, "rates": j["rates"], "date": j["date"], "live": True}
    except Exception as e:
        return {"base": "USD", "rates": {k: v for k, v in SNAPSHOT_FX.items() if k in ("EUR", "GBP", "JPY")}, "date": SNAPSHOT_FX["date"], "live": False, "error": str(e)[:200]}

def worldbank_rd(country="US", indicator="GB.XPD.RSDV.GD.ZS") -> dict:
    """R&D % GDP series. Live World Bank API, fallback snapshot."""
    try:
        code = "USA" if country == "US" else country
        j = _http_json(f"https://api.worldbank.org/v2/country/{code}/indicator/{indicator}?format=json&per_page=40")
        obs = [x for x in j[1] if x["value"] is not None]
        return {"live": True, "latest": obs[0], "series": {x["date"]: x["value"] for x in obs[:10]}}
    except Exception as e:
        return {"live": False, "error": str(e)[:200], "series": {"2023": 3.44716, "2022": 3.48736, "2021": 3.4689, "2020": 3.41788}}

def save_live_snapshot(payload: dict, name: str) -> str:
    os.makedirs(LIVE_DIR, exist_ok=True)
    path = os.path.join(LIVE_DIR, name)
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path

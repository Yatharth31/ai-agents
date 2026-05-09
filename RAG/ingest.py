"""Ingest utilities for the RAG project using AlphaVantage weekly-adjusted data.

This module fetches weekly adjusted time series via the helper in `test.py`,
saves processed JSON documents under `data/processed/`, and creates short
textual documents for embedding and optional upsert into the vectorstore.
"""
import os
import json
from datetime import datetime, timezone
from typing import List, Optional
from pathlib import Path

# local imports
import fetch_data
import embeddings as emb_module
import vectorstore as vs


DATA_RAW = os.path.join(os.getcwd(), "data", "raw")
DATA_PROCESSED = os.path.join(os.getcwd(), "data", "processed")


def ensure_dirs() -> None:
    os.makedirs(DATA_RAW, exist_ok=True)
    os.makedirs(DATA_PROCESSED, exist_ok=True)


def save_processed(doc: dict, prefix: str = "weekly") -> str:
    ensure_dirs()
    now = datetime.now(timezone.utc).isoformat()
    safe_ts = now.replace(':', '-')
    symbol = doc.get('symbol', prefix)
    fname = f"{symbol}_{prefix}_{safe_ts}.json"
    out_path = os.path.join(DATA_PROCESSED, fname)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2, default=str)
    return out_path


def ingest_weekly(symbol: str, save_json: bool = True, outdir: Optional[str] = None, n_weeks: Optional[int] = 52, upsert: bool = True):
    """Fetch weekly-adjusted time series for `symbol`, save JSON and optionally upsert docs.

    - `n_weeks`: number of most recent weeks to process (default 52). Use None for all.
    - `upsert`: when True, compute embeddings and upsert into chroma vectorstore
    Returns a dict with keys: `json` (path or None), `n_docs`, `ids`.
    """
    if outdir is None:
        outdir = DATA_PROCESSED
    Path(outdir).mkdir(parents=True, exist_ok=True)

    df = fetch_data.get_weekly_adjusted(symbol)

    # Convert dataframe to a dict with string keys (JSON requires string keys)
    raw_data = df.to_dict(orient='index')
    data_as_strings = {str(k): v for k, v in raw_data.items()}
    payload = {
        'symbol': symbol,
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'source': 'alphavantage_weekly_adjusted',
        'data': data_as_strings,
    }

    json_path = None
    if save_json:
        json_path = save_processed(payload, prefix='weekly_adjusted')

    # slice most recent weeks
    df_proc = df.tail(n_weeks) if n_weeks else df

    # create simple textual documents per-week
    docs = []
    metadatas = []
    for idx, row in df_proc.iterrows():
        date_str = idx.strftime('%Y-%m-%d')
        text = (
            f"{symbol} weekly summary for {date_str}: open {row.get('open')}, "
            f"high {row.get('high')}, low {row.get('low')}, close {row.get('close')}, "
            f"adjusted close {row.get('adjusted close')}, volume {int(row.get('volume', 0))}."
        )
        docs.append(text)
        metadatas.append({
            "symbol": symbol,
            "date": date_str,
            "source": "alphavantage_weekly_adjusted",
        })

    ids = []
    if upsert and docs:
        embeddings = emb_module.embed_texts(docs)
        ids = vs.upsert(docs=docs, embeddings=embeddings, metadatas=metadatas)
        print(ids)

    return {"json": json_path, "n_docs": len(docs), "ids": ids}



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", "-t", nargs="+", default=[], help="Ticker symbols to ingest (uses AlphaVantage weekly)")
    parser.add_argument("--weekly", "-w", nargs="+", help="Fetch weekly adjusted for given symbols (AlphaVantage)")
    parser.add_argument("--no-save-json", action="store_true", help="Do not save weekly JSON")
    parser.add_argument("--no-upsert", action="store_true", help="Do not upsert weekly docs into vectorstore")
    parser.add_argument("--n-weeks", type=int, default=52, help="How many recent weeks to include (default 52). Use 0 for all)")
    args = parser.parse_args()

    if args.tickers:
        out = ingest(args.tickers)
        print("Saved:")
        for p in out:
            print(" -", p)

    if args.weekly:
        for s in args.weekly:
            n_weeks = args.n_weeks if args.n_weeks != 0 else None
            res = ingest_weekly(s, save_json=(not args.no_save_json), upsert=(not args.no_upsert), n_weeks=n_weeks)
            print(f"Weekly ingest for {s}: saved_json={res['json']}, docs={res['n_docs']}")

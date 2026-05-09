# RAG Market Data Prototype

This repository contains a minimal Retrieval-Augmented Generation (RAG) prototype focused on market data.

Quick start

1. Create a Python virtualenv and install requirements:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Ingest a ticker (example):

```bash
python RAG/ingest.py --tickers AAPL
```

3. Start the Streamlit app:

```bash
streamlit run RAG/app.py
```
Project flow (high-level)
-------------------------

Files and responsibilities:
- [RAG/fetch_data.py](RAG/fetch_data.py): contains `get_weekly_adjusted()` which calls the AlphaVantage API (`TIME_SERIES_WEEKLY_ADJUSTED`) and returns a pandas DataFrame.
- [RAG/ingest.py](RAG/ingest.py): orchestrates ingestion. `ingest_weekly()` calls `fetch_data.get_weekly_adjusted()`, saves the weekly data as JSON under `data/processed/`, builds short per-week textual documents, and optionally computes embeddings and upserts them to the vectorstore.
- [RAG/embeddings.py](RAG/embeddings.py): wraps `SentenceTransformer` to convert texts into vector embeddings (`embed_texts()`).
- [RAG/vectorstore.py](RAG/vectorstore.py): thin wrapper around ChromaDB; provides `upsert()` and `query_by_embedding()` helper functions.
- [RAG/app.py](RAG/app.py): Streamlit UI. It can call `ingest()` for quick ingest and uses the embedding + vectorstore helpers to run similarity search for queries.

Typical execution flows
----------------------

1) Ingest weekly data (JSON + docs)
	- `RAG/ingest.py` -> calls -> `RAG/fetch_data.py:get_weekly_adjusted()`
	- Saves JSON to `data/processed/` (filename like `SYMBOL_weekly_adjusted_<timestamp>.json`).
	- Produces per-week short text documents (one per weekly row) used for embedding.

2) Build embeddings and upsert (optional)
	- `RAG/ingest.py` calls `RAG/embeddings.py:embed_texts()` to compute vectors.
	- Vectors + docs + metadata are written to Chroma via `RAG/vectorstore.py:upsert()`.

3) Query via Streamlit UI
	- `RAG/app.py` embeds the user query with `RAG/embeddings.py` and runs `RAG/vectorstore.py:query_by_embedding()` to retrieve nearest docs.

Quick commands
--------------

- Ingest a ticker (save JSON, no upsert):

```bash
python RAG/ingest.py --weekly IBM --no-upsert
```

- Ingest and upsert (compute embeddings and add to Chroma):

```bash
python RAG/ingest.py --weekly IBM
```

- Run the Streamlit UI:

```bash
streamlit run RAG/app.py
```

Where data lands
----------------
- Raw / processed JSON documents: `data/processed/`
- Local Chroma DB (persisted): `db/chroma/`

Notes & next steps
-------------------
- If you plan to ingest frequently, rotate filenames or add dedup logic in `RAG/ingest.py`.
- For larger scale ingestion, add batching and parallel embedding.
- Consider adding unit tests for `RAG/fetch_data.py` and `RAG/ingest.py` (there is a starter test at `RAG/tests/`).

If you want, I can:
- Upsert the files we already fetched into Chroma now.
- Add a small example notebook that queries the vectorstore.
- Add automated tests for the ingest flow.

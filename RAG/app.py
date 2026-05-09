"""Streamlit app for querying the local RAG vectorstore."""
import os
from typing import List

import streamlit as st

from embeddings import embed_texts
import vectorstore


st.set_page_config(page_title="Market RAG QA", layout="wide")

st.title("Market Data RAG — Retrieval UI")

with st.sidebar:
    st.header("Ingest")
    ticker = st.text_input("Ticker to ingest", value="AAPL")
    if st.button("Ingest ticker"):
        from ingest import ingest_weekly

        paths = ingest_weekly(ticker.strip().upper())
        st.success(f"Saved {len(paths)} document(s)")

    st.markdown("---")
    st.header("Query")
    k = st.slider("Top k", min_value=1, max_value=10, value=5)

query = st.text_input("Enter your query")
if st.button("Search") and query.strip():
    # embed the query
    q_emb = embed_texts([query])[0]
    res = vectorstore.query_by_embedding(q_emb, k=k)
    # chroma returns dicts with ids, documents, metadatas, distances
    docs: List[str] = res.get("documents", [[]])[0]
    metas: List[dict] = res.get("metadatas", [[]])[0]
    dists: List[float] = res.get("distances", [[]])[0]

    st.write(f"Found {len(docs)} results")
    for i, (doc, meta, dist) in enumerate(zip(docs, metas, dists), start=1):
        st.subheader(f"Result {i} — score {dist:.4f}")
        st.write(doc)
        st.markdown(f"**Ticker:** {meta.get('ticker', '')}  |  **Source:** {meta.get('source','')}  |  **Fetched:** {meta.get('fetched_at','')}")

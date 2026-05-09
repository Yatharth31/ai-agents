"""RAG package for market-data retrieval-augmented generation prototype.

This package exposes lightweight modules for ingestion, embeddings,
vectorstore operations, a Streamlit app, and transformer-based NER.
"""

__version__ = "0.1.0"

from . import ingest, embeddings, vectorstore, app, ner

__all__ = [
    "ingest",
    "embeddings",
    "vectorstore",
    "app",
    "__version__",
]

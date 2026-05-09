"""Simple Chroma-backed vector store helper."""
import os
from uuid import uuid4
from typing import List, Dict, Any

import os
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"

import chromadb
from chromadb.config import Settings

PERSIST_DIR = "db/chroma"


def _get_client():
    # Use persisted chroma DB in PERSIST_DIR
    settings = Settings(persist_directory=PERSIST_DIR)
    return chromadb.Client(settings=settings)


def _get_collection(client, name: str = "market_docs"):
    return client.get_or_create_collection(name=name)


def upsert(docs: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], ids: List[str] = None) -> List[str]:
    client = _get_client()
    col = _get_collection(client)
    print(col)
    col.add(documents=docs, embeddings=embeddings, metadatas=metadatas, ids=[str(uuid4()) for _ in docs])
    client.persist()

    return None


def query_by_embedding(embedding: List[float], k: int = 5):
    client = _get_client()
    col = _get_collection(client)
    res = col.query(query_embeddings=[embedding], n_results=k)
    return res

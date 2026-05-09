"""Embedding utilities using SentenceTransformers."""
from typing import List

from sentence_transformers import SentenceTransformer

_MODEL_NAME = "all-MiniLM-L6-v2"
_MODEL = None


def _get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(_MODEL_NAME)
    return _MODEL


def embed_texts(texts: List[str]):
    """Return list of embeddings for input texts."""
    model = _get_model()
    embs = model.encode(texts, show_progress_bar=False)
    return embs.tolist()

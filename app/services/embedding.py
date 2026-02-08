"""
Embedding service.
Encapsulates embedding logic so it can be reused
and swapped easily if needed.
"""

from app.core.models import embedder

def embed_text(text: str):
    """
    Converts text into a normalized vector embedding.
    Normalization improves cosine similarity accuracy.
    """
    return embedder.encode(text, normalize_embeddings=True)

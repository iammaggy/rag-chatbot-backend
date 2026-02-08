"""
Utility helpers related to text processing.
"""
import re
from typing import List

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> list[str]:
    """
    Splits large text into overlapping chunks.
    This improves semantic retrieval accuracy.

    Args:
        text: Raw input text
        chunk_size: Number of words per chunk
        overlap: Overlapping words between chunks

    Returns:
        List of text chunks
    """
    if not text or not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks: List[str] = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk_words = words[start:start + chunk_size]
        if chunk_words:
            chunks.append(" ".join(chunk_words))

    return chunks


    return chunks

def clean_snippet(text: str) -> str:
    """
    Removes DDG time prefixes like '1 day ago -'
    """
    return re.sub(r"^\d+\s+(day|days|week|weeks|month|months|year|years)\s+ago\s+-\s+", "", text).strip()

"""
Centralized configuration file.
All tunable values live here so they can be adjusted
without touching business logic.
"""

# Embedding & LLM models
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"
LLM_MODEL = "google/flan-t5-base"

# Retrieval & generation tuning
TOP_K = 3
SIMILARITY_THRESHOLD = 0.5
MAX_GEN_TOKENS = 150

"""
This module is responsible for loading ML models.
Models are loaded only once at application startup
to avoid repeated heavy initialization per request.
"""

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from app.core.config import EMBED_MODEL, LLM_MODEL

# Load sentence embedding model (used for vector similarity search)
embedder = SentenceTransformer(EMBED_MODEL, device="cpu")

# Load tokenizer & LLM for text generation
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL)

# Create inference pipeline
llm = pipeline("text2text-generation", model=model, tokenizer=tokenizer, do_sample=False)

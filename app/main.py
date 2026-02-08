"""
Application entry point.
Initializes FastAPI and registers routes & middleware.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chatbot

app = FastAPI(title="RAG Chatbot API")

import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# Enable CORS (use stricter settings in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(chatbot.router)

"""
API routes for chatbot operations.
Routes are thin and delegate logic to services.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.chat import AskItem, Para, KnowledgeResponse
from app.db.db_con import SessionLocal
from app.models.knowledge import Knowledge
from app.services.embedding import embed_text
from app.services.search import search_knowledge, web_search
from app.services.llm import generate_answer
from app.utils.text import chunk_text
from typing import List

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


def get_db():
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_data")
async def add_data(payload: Para, db: Session = Depends(get_db)):
    """
    Stores input text into the vector database
    after chunking and embedding.
    """
    chunks = chunk_text(payload.text)

    for idx, chunk in enumerate(chunks):
        db.add(
            Knowledge(
                content=chunk,
                embedding=embed_text(chunk),
                chunk_index=idx
            )
        )

    db.commit()
    return {"status": "stored"}


@router.post("/ask")
async def ask_question(payload: AskItem, db: Session = Depends(get_db)):
    """
    Answers a question using:
    1. Vector search (preferred)
    2. Web search fallback
    """
    results = search_knowledge(db, payload.question)

    # Web fallback if no vector context found
    
    if not results:
        answer, context = await web_search(payload.question)
        return {"answer": answer, "context_used": context}

    # Combine retrieved chunks
    context = "\n".join(r[0] for r in results)

    prompt = f"""
    Answer the question using only the information in the context.

    Context:
    {context}

    Question:
    {payload.question}

    Answer:
    """.strip()
    
    return {
        "answer": generate_answer(prompt),
        "context_used": context
    }

@router.get("/stored_knowledge", response_model=List[KnowledgeResponse])
def get_all_knowledge(db: Session = Depends(get_db)):
    records = db.query(Knowledge).order_by(Knowledge.created_at.desc()).all()
    return records

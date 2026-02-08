"""
Handles knowledge base search and web fallback logic.
"""

from sqlalchemy.orm import Session
from ddgs import DDGS

from app.models.knowledge import Knowledge
from app.core.config import SIMILARITY_THRESHOLD, TOP_K
from app.services.embedding import embed_text
from app.services.llm import generate_answer
from app.utils.text import clean_snippet


def search_knowledge(db: Session, question: str):
    """
    Searches the vector database using cosine similarity.
    """
    q_emb = embed_text(question)

    # pgvector cosine distance search
    distance = Knowledge.embedding.cosine_distance(q_emb)

    return (
        db.query(Knowledge.content, distance.label("distance"))
        .filter(distance < SIMILARITY_THRESHOLD)
        .order_by(distance)
        .limit(TOP_K)
        .all()
    )


async def web_search(question: str):
    # snippets = []

    # with DDGS() as ddgs:
    #     for r in ddgs.text(question, max_results=5):
    #         body = r.get("body")
    #         if body:
    #             snippets.append(body.strip())

    # if not snippets:
    #     return "I don't know", ""

    # context = "\n".join(snippets[:2])

    # prompt = f"""
    # Answer the question using the context below.

    # Context:
    # {context}

    # Question:
    # {question}

    # Answer:
    # """.strip()

    # answer = generate_answer(prompt)
    # # return answer, context

    snippets = []

    with DDGS() as ddgs:
        for r in ddgs.text(question, max_results=5):
            if r.get("body"):
                snippets.append(clean_snippet(r["body"]))

    if not snippets:
        return {
            "answer": "I don't know",
            "context": ""
        }

    context = "\n".join(snippets[:3])

    prompt = f"""
        You are a factual question answering assistant.

        Use ONLY the context below.
        Extract the direct factual answer.
        Do NOT summarize.
        Do NOT include dates, headlines, or extra explanations.
        If the answer is not clearly present, reply with "I don't know."

        Context:
        {context}

        Question:
        {question}

        Answer (one short sentence or name only):
    """.strip()
    return generate_answer(prompt), context



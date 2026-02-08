"""
LLM inference service.
Responsible only for generating answers.
"""

from app.core.models import llm
from app.core.config import MAX_GEN_TOKENS

def generate_answer(prompt: str) -> str:
    """
    Generates a response using the LLM based on a prompt.
    """
    response = llm(
        prompt,
        max_new_tokens=50,
        temperature=0.7,
        do_sample=True,
    )
    text = response[0]["generated_text"]

    # 🔥 Remove prompt echo safely
    if text.startswith(prompt):
        text = text[len(prompt):]

    return text.strip()

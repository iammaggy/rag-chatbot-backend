from pydantic import BaseModel
from datetime import datetime
from typing import List


class AskItem(BaseModel):
    question: str
    top_k: int = 3

class Para(BaseModel):
    text: str


class KnowledgeResponse(BaseModel):
    id: int
    content: str
    chunk_index: int
    created_at: datetime

    class Config:
        orm_mode = True

class KnowledgeWithEmbeddingResponse(KnowledgeResponse):
    embedding: List[float]

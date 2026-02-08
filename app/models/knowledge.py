from sqlalchemy import Column, Integer, Text, JSON, TIMESTAMP, func
from pgvector.sqlalchemy import Vector
from ..db.db_con import Base

class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768), nullable=False)  # pgvector column
    created_at = Column(TIMESTAMP, server_default=func.now())
    chunk_index = Column(Integer, nullable=False) 

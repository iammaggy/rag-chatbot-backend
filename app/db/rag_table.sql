CREATE DATABASE rag_chatbot_db;
CREATE USER raguser WITH PASSWORD 'ragpass';
GRANT ALL PRIVILEGES ON DATABASE rag_chatbot_db TO raguser;

\c rag_chatbot_db

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE knowledge (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(384),
    chunk_index INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- For cosine similarity to make search faster
CREATE INDEX knowledge_embedding_idx
ON knowledge
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

ANALYZE knowledge;

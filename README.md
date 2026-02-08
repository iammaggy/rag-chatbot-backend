# 🤖 AI Chatbot with Knowledge Base

A FastAPI-based intelligent chatbot that combines a local knowledge base with web search capabilities. The system uses sentence transformers for semantic search and retrieval-augmented generation (RAG) for accurate question answering.

## ✨ Features

- **Knowledge Base Management**: Store and retrieve information using vector embeddings
- **Semantic Search**: Find relevant content using cosine similarity
- **Web Search Fallback**: Automatically searches the web when local knowledge is insufficient
- **Text Chunking**: Intelligently splits large texts for better retrieval
- **Grammar Correction**: Built-in grammar correction capabilities
- **RESTful API**: Clean, well-documented API endpoints
- **Scalable Architecture**: Service-layer design pattern for easy maintenance

## 🏗️ Architecture

```
app/
├── api/                        # API route definitions
│   ├── __init__.py
│   └── chatbot.py              # Chatbot-related endpoints (/ask, /add_data)
│
├── core/                       # Core application configuration & ML models
│   ├── __init__.py
│   ├── config.py               # Environment variables & constants
│   └── models.py               # LLM & embedding model initialization
│
├── db/                         # Database setup and session handling
│   ├── __init__.py
│   └── session.py              # SQLAlchemy DB session (renamed from db_con.py)
│
├── models/                     # ORM models
│   ├── __init__.py
│   └── knowledge.py            # Knowledge table (pgvector embeddings)
│
├── services/                   # Business logic & RAG pipeline
│   ├── __init__.py
│   ├── embedding.py            # Text → vector embeddings
│   ├── llm.py                  # LLM inference layer
│   └── search.py               # Vector search + web fallback logic
│
├── utils/                      # Shared utility functions
│   ├── __init__.py
│   └── text.py                 # Text chunking & preprocessing
│
├── main.py                     # FastAPI app entry point
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
     
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip or poetry

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd chatbot-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```python
   from app.db.db_con import init_db
   init_db()
   ```

### Running the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

or

python -m uvicorn app.main:app --workers 1
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## 📡 API Endpoints

### Add Data to Knowledge Base
```http
POST /chatbot/add_data
Content-Type: application/json

{
  "text": "Your text content here..."
}
```

### Ask a Question
```http
POST /chatbot/ask
Content-Type: application/json

{
  "question": "What is machine learning?",
  "top_k": 3
}
```

### Health Check
```http
GET /chatbot/health
```

### Admin: View Embeddings
```http
GET /chatbot/admin_transform_data
```

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./kb.sqlite3` |
| `EMBED_MODEL` | Sentence transformer model | `sentence-transformers/all-mpnet-base-v2` |
| `LLM_MODEL` | Text generation model | `google/flan-t5-base` |
| `TOP_K` | Number of results to retrieve | `3` |
| `SIMILARITY_THRESHOLD` | Cosine similarity threshold | `0.5` |
| `CHUNK_SIZE` | Text chunk size in words | `400` |
| `CHUNK_OVERLAP` | Overlap between chunks | `50` |

## 🧪 Usage Examples

### Python Client

```python
import requests

BASE_URL = "http://localhost:8000"

# Add knowledge
response = requests.post(
    f"{BASE_URL}/chatbot/add_data",
    json={"text": "Machine learning is a subset of AI..."}
)
print(response.json())

# Ask question
response = requests.post(
    f"{BASE_URL}/chatbot/ask",
    json={"question": "What is machine learning?", "top_k": 3}
)
print(response.json())
```

### cURL

```bash
# Add data
curl -X POST "http://localhost:8000/chatbot/add_data" \
  -H "Content-Type: application/json" \
  -d '{"text": "Python is a programming language..."}'

# Ask question
curl -X POST "http://localhost:8000/chatbot/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?", "top_k": 3}'
```

## 🏗️ Project Structure

### Services Layer
- **EmbeddingService**: Handles text-to-vector conversion
- **LLMService**: Manages text generation and grammar correction
- **TextProcessingService**: Text chunking and cleaning
- **KnowledgeBaseService**: Knowledge base CRUD operations
- **WebSearchService**: Web search integration
- **AnswerGenerationService**: Answer generation from context

### Database Models
- **Knowledge**: Stores text chunks with vector embeddings

### Schemas
Pydantic models for request/response validation and serialization

## 🔒 Security Considerations

- Use strong `ADMIN_TOKEN` in production
- Enable HTTPS in production deployments
- Consider rate limiting for public APIs
- Sanitize user inputs
- Use environment variables for secrets

## 🚀 Deployment

### Docker (Recommended)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t chatbot-api .
docker run -p 8000:8000 --env-file .env chatbot-api
```

### Cloud Deployment

Compatible with:
- AWS (ECS, Lambda)
- Google Cloud (Cloud Run, App Engine)
- Azure (Container Instances, App Service)
- Heroku
- Railway
- Render

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_chatbot.py::test_add_data
```

## 📊 Performance Optimization

- Model caching: Models are loaded once and reused
- Singleton services: Services are instantiated once
- Database connection pooling
- Batch processing for multiple embeddings
- Efficient text chunking with overlap

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Run `black` for formatting
- Run `flake8` for linting

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Sentence Transformers for embeddings
- Hugging Face for transformer models
- DuckDuckGo for web search API
- FastAPI for the web framework

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🔮 Future Enhancements

- [ ] Add authentication and user management
- [ ] Implement conversation history
- [ ] Add support for multiple languages
- [ ] Integrate more LLM providers (OpenAI, Anthropic)
- [ ] Add document upload (PDF, DOCX)
- [ ] Implement caching layer (Redis)
- [ ] Add monitoring and analytics
- [ ] Create web UI dashboard
- [ ] Support for images and multimodal input
- [ ] Add vector database support (Pinecone, Weaviate)

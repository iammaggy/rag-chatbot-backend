from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------
# Database Configuration
# -------------------------------------------------

# PostgreSQL connection string
# Format: postgresql://<user>:<password>@<host>:<port>/<db_name>
DATABASE_URL = "postgresql://raguser:ragpass@localhost:5432/rag_chatbot_db"

# Create SQLAlchemy engine
# echo=True enables SQL query logging (use False in production)
engine = create_engine(
    DATABASE_URL,
    echo=True,            # Log SQL queries (set False in prod)
    pool_pre_ping=True    # Checks DB connection health
)

# -------------------------------------------------
# Session Factory
# -------------------------------------------------

# Each request will get its own database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# -------------------------------------------------
# Base class for ORM models
# -------------------------------------------------

# All SQLAlchemy models should inherit from this Base
Base = declarative_base()

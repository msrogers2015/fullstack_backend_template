# configs/database_test.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.BaseModel import BaseModel

# Use in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create all tables based on model definitions
BaseModel.metadata.create_all(bind=engine)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

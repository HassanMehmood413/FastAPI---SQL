from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

# Database connection URL (SQLite in this case)
SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///./blogs.db"

# Create the engine for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 2. Create a session maker
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

engine = create_engine(settings.DATABASE_URL,
                       pool_size=20, # Adjust pool size
                       max_overflow=10, # Allow extra connections beyond pool size
                       pool_timeout=30 # Timeout for getting a connection from the pool
                       )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

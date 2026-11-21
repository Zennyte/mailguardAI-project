from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Zgjedhim driver-in psycopg2 qe ne requirements.txt (SQLAlchemy 2.1+ do te perdorte nje driver tjeter si default)
database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa baze per te gjitha modelet SQLAlchemy
Base = declarative_base()


# Cdo kerkese merr nje session te ri te databazes dhe e mbyll ne fund
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

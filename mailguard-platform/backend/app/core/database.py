from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Klasa baze per te gjitha modelet SQLAlchemy
Base = declarative_base()


def get_db():
    # Cdo kerkese merr nje session te ri dhe e mbyll ne fund
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

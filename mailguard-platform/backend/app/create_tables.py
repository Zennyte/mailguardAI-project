"""
Script i thjeshte qe krijon te gjitha tabelat ne PostgreSQL.

Perdorim:
    cd backend
    python -m app.create_tables

Databaza 'mailguard_platform' duhet te ekzistoje me pare ne PostgreSQL.
"""
from app.core.database import Base, engine
from app import models  # noqa: F401 - importon te gjitha modelet


def main():
    print(f"Creating {len(Base.metadata.tables)} tables ...")
    Base.metadata.create_all(bind=engine)
    print("Done. All tables created.")


if __name__ == "__main__":
    main()

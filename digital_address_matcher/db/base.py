from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Engine


DB_URL: str = "postgresql://postgres:12345678@127.0.0.1:5432/test_db"

engine: Engine = create_engine(DB_URL)
DBSession = sessionmaker(bind=engine) 

def get_db():
    """Зависимость."""
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
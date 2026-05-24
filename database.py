from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///./forge_db.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
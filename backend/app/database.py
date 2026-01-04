from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings 
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_url)

sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally: 
        db.close()
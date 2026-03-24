from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(str(settings.DATABASE_URL))

# Create local session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


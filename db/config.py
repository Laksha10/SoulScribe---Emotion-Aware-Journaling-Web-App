# db/config.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres@localhost/soulscribe_db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

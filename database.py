from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import setting


SQL_ALCHEMY_DB_URL = (f"postgresql://{setting.db_usr}:"
                      f"{setting.db_pwd}@{setting.db_host}:"
                      f"{setting.db_port}/{setting.db_name}")

engine = create_engine(SQL_ALCHEMY_DB_URL, pool_size=100, max_overflow=200)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

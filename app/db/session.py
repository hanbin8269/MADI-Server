from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.config import settings
from app.model import Base

DATABASE = settings.SQLALCHEMY_DATABASE_URI

ENGINE = create_engine(DATABASE, encoding="utf-8", echo=False)
Base.metadata.create_all(ENGINE)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from yakoon.domains.gateway.stores.___sql._base import Base

engine = create_engine("sqlite:///yakoon.db", echo=False)
LocalSqlSession = sessionmaker(bind=engine)


def create_missing_tables():
    """
    Creates all ORM-defined tables that do not already exist in the database.
    Does not alter or remove any existing structures.
    """
    Base.metadata.create_all(bind=engine)

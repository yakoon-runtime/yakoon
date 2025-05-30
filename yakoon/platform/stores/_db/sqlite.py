from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from yakoon.platform.stores.sql._base import Base

# Engine-Setup + SessionFactory
engine = create_engine("sqlite:///yakoon.db", echo=False)
SessionLocal = sessionmaker(bind=engine)

# Tabellen erzeugen (einmalig beim Start)
def init_db():
    Base.metadata.create_all(bind=engine)

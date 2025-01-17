from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/shift"

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)


def init_db():
    """This is used to initialize the tables in the db on startup"""
    Base.metadata.create_all(engine)
    print("Database connected and tables created.")


def get_session():
    """"This is used to return the session (actual connection) to the db.  """
    return Session()

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = "sqlite:///users.db"  # Use SQLite for simplicity, you can change to your database URL

Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


# Create an engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create the tables (if not already created)
Base.metadata.create_all(engine)

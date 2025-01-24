import json

from sqlalchemy import Column, Integer, String
from .db import db


# Define the User model
class User(db.Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    def __repr__(self) -> str:
        # Convert from dict to str
        return json.dumps({"id": self.id, "username": self.username})

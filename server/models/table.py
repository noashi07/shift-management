import json

from sqlalchemy import Column, Integer, String
from .db import db


# Define the User model
class TableData(db.Base):
    __tablename__ = 'table_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String(255), nullable=False)
    column = Column(Integer, nullable=False)
    row = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        # Convert from dict to str
        return json.dumps({"id": self.id, "data": self.data, "column": self.column, "row": self.row})

from sqlalchemy import Column, Integer, String

from app.db.session import Base
from pydantic import BaseModel


# SQLAlchemy ORM model - maps to the "items" table in MySQL
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)


# -------- Pydantic schemas for FastAPI --------

class ItemBase(BaseModel):
    name: str


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int

    class Config:
        orm_mode = True


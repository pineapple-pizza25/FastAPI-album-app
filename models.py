from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    artist = Column(String)
    rating = Column(Integer)
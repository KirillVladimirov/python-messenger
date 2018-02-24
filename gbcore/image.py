
from sqlalchemy import Column, Integer, BLOB
from gbcore.base import Base


class Image(Base):

    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    Data = Column(BLOB)

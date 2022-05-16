from sqlalchemy import Column, Integer, String, Float
from .database import Base


class AddressBook(Base):
    __tablename__ = "address_book"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    lattitude = Column(Float)
    longitude = Column(Float)

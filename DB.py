from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase


engine = create_engine('sqlite:///mock_data.db')

class Base(DeclarativeBase):
    pass

class mock_table(Base):
    __tablename__ = 'mock_table'

    id = Column(Integer, primary_key=True)
    timestamp = Column(String(20), unique=False, nullable=False)
    latitude = Column(Float, unique=False, nullable=False)
    longitude = Column(Float, unique=False, nullable=False)
    speed = Column(Float, unique=False, nullable=False)

Base.metadata.create_all(engine)

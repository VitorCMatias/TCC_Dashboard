from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine('sqlite:///./mock_data.db')
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class mock_table(Base):
    __tablename__ = 'mock_table'

    id = Column(Integer, primary_key=True)
    timestamp = Column(String(20), unique=False, nullable=False)
    latitude = Column(Float, unique=False, nullable=False)
    longitude = Column(Float, unique=False, nullable=False)
    speed = Column(Float, unique=False, nullable=False)

def save(gps_datetime, longitude, latitude, speed):
    db: Session = SessionLocal()
    db_data = mock_table(timestamp=gps_datetime, longitude=longitude, latitude=latitude, speed=speed)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()

Base.metadata.create_all(engine)

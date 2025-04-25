from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()


class Signal(Base):
    __tablename__ = "signal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)          
    timestamp = Column(DateTime, nullable=False)   
    signal_id = Column(Integer, nullable=False)    
    value = Column(Float, nullable=True)           

    def __repr__(self):
        return f"<Signal {self.name} @ {self.timestamp} = {self.value}>"

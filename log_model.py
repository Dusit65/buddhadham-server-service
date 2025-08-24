from sqlalchemy import NVARCHAR, Column, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Log(Base):
    __tablename__ = "log_tb"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(NVARCHAR(None))
    createdAt = Column(DateTime, default=datetime.now)
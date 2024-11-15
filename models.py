from sqlalchemy import Column, Integer, VARCHAR, DateTime
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(30), nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    name = Column(VARCHAR(10), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(VARCHAR(2), nullable=False)
    job = Column(VARCHAR(30), nullable=False)
    further_details = Column(VARCHAR(100), nullable=True)
    prefer_task = Column(VARCHAR(100), nullable=True)
    registered_at = Column(DateTime, nullable=False, default=datetime.now)
    modified_at = Column(DateTime, nullable=True)


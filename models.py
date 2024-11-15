from typing import Optional

from sqlalchemy import Column, Integer, VARCHAR, DateTime, TEXT, ForeignKey, PrimaryKeyConstraint
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
    work_life_ratio = Column(VARCHAR(10), nullable=False)
    job = Column(VARCHAR(30), nullable=False)
    further_details = Column(VARCHAR(100), nullable=True)
    prefer_task = Column(VARCHAR(100), nullable=True)
    registered_at = Column(DateTime, nullable=False, default=datetime.now)
    modified_at = Column(DateTime, nullable=True)


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    type = Column(VARCHAR(10), nullable=False)
    title = Column(VARCHAR(30), nullable=False)
    body = Column(TEXT, nullable=False)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)


class TaskRelation(Base):
    __tablename__ = "TaskRelation"

    task_id = Column(Integer)
    sub_task_id = Column(Integer)

    __table_args__ = (
        PrimaryKeyConstraint(task_id, sub_task_id),
        {},
    )


class TaskHistory(Base):
    __tablename__ = "TaskHistory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, nullable=False)
    type = Column(VARCHAR(10), nullable=False)
    title = Column(VARCHAR(30), nullable=False)
    body = Column(TEXT, nullable=False)
    status = Column(VARCHAR(10), nullable=False)
    start = Column(DateTime, nullable=True)
    end = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

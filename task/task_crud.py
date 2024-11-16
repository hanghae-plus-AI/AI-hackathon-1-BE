from sqlalchemy.orm import Session
from datetime import datetime
from models import Task, TaskHistory
from task import task_schema

from task.task_schema import NewTask, NewTaskHistory


def get_task(id: int, db: Session):
    return db.query(Task).filter(NewTask.id == id, NewTask.type == "TASK").first()


def get_tasks(start: datetime, end: datetime, db: Session):
    return db.query(Task).where(Task.start <= start).where(Task.end >= end).all()


def create_task(create_task_req: task_schema.CreateTaskReq, user_id: str, db: Session):
    new_task = Task(
        user_id=user_id,
        type=create_task_req.type,
        title=create_task_req.title,
        body=create_task_req.body,
        start=datetime.utcfromtimestamp(create_task_req.start),
        end=datetime.utcfromtimestamp(create_task_req.end)
    )
    db.add(new_task)
    db.commit()
    return new_task


def update_task(update_task_req: task_schema.UpdateTaskReq, db: Session):
    new_task = Task(
        id=update_task.id,
        type=update_task_req.type,
        title=update_task_req.title,
        body=update_task_req.body,
        start=datetime.utcfromtimestamp(update_task_req.start),
        end=datetime.utcfromtimestamp(update_task_req.end)
    )
    db.query(Task).filter(Task.id == update_task_req.id).update(new_task)
    db.commit()
    return new_task


def delete_task(id: int, db: Session):
    subtask = get_task(id, db)
    if subtask:
        # Create task history record
        history = NewTaskHistory(
            task_id=id,
            type="NORMAL",
            content=subtask.content,
            detail=subtask.detail,
            start=subtask.start or datetime.now(),
            end=subtask.end or datetime.now(),
            status="DELETED"
        )
        db.add(history)

        # Delete subtask
        db.delete(subtask)
        db.commit()
        return True
    return False

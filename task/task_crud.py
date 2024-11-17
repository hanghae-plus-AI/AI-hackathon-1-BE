from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime
from models import Task, TaskHistory
from task import task_schema

from task.task_schema import NewTask, NewTaskHistory


def get_task(id: int, db: Session):
    return db.query(Task).filter(Task.id == id, Task.type == "TASK").first()


def get_tasks(start: datetime, end: datetime, db: Session):
    return db.query(Task).all() \
        # .filter(Task.start <= start) \
        # .filter(Task.start <= end) \
        # .filter(Task.end >= start) \
        # .filter(Task.end >= end) \
        # .filter(or_(Task.start >= start & Task.start <= end)) \
        # .filter(or_(Task.end >= start & Task.end <= end)) \
        # .all()


def create_task(create_task_req: task_schema.CreateTaskReq, user_id: str, db: Session):
    new_task = Task(
        user_id=user_id,
        type=create_task_req.type,
        title=create_task_req.title,
        body=create_task_req.body,
        start=create_task_req.start,
        end=create_task_req.end
    )
    db.add(new_task)
    db.commit()
    return new_task


def update_task(update_task_req: task_schema.UpdateTaskReq, db: Session):
    new_task = Task(
        id=update_task_req.id,
        type=update_task_req.type,
        title=update_task_req.title,
        body=update_task_req.body,
        start=update_task_req.start,
        end=update_task_req.end
    )

    db.commit()
    return new_task


def delete_task(id: int, db: Session):
    task: Task = get_task(id, db)
    if task.type == 'TASK':
        tasks: list[Task] = db.query(Task).where(Task.id == task.id).all()

        # bulk_insert_mappings 를 나중에 적용하면 좋을 듯
        for delSubTask in tasks:
            db.add(TaskHistory().make_new_task_history_of(delSubTask))
        db.query(Task).where(Task.id == task.id).delete()

    if task:
        # Create task history record
        history = TaskHistory(
            task_id=id,
            type="NORMAL",
            content=task.content,
            detail=task.detail,
            start=task.start or datetime.now(),
            end=task.end or datetime.now(),
            status="DELETED"
        )
        db.add(history)

        # Delete subtask
        db.delete(task)
        db.commit()
        return True
    return False

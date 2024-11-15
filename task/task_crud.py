from sqlalchemy.orm import Session
from datetime import datetime
from models import Task, TaskHistory

from task.task_schema import NewTask, NewTaskHistory

def get_task(id: int, db: Session):
    return db.query(Task).filter(NewTask.id == id, NewTask.type == "TASK").first()

def get_subtask(id: int, db: Session):
    return db.query(NewTask).filter(NewTask.id == id, NewTask.type == "SUBTASK").first()


def delete_subtask(id: int, db: Session):
    subtask = get_subtask(id, db)
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
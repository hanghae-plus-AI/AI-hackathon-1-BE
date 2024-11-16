from datetime import datetime
import json
from typing import Dict, Any, Annotated
from task import task_schema, task_crud
from user import user_schema, user_crud
from models import User

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Header

from database import get_db
from ai import model

app = APIRouter(prefix="/task")


@app.post("")
async def post_task(
        create_task_req: task_schema.CreateTaskReq, db: Session = Depends(get_db),
        authorization: Annotated[str | None, Header()] = "1"
) -> Dict[str, Any]:
    selectUser: User = user_crud.get_user_by_autoincrement(int(authorization), db)
    print(selectUser)

    subtasks = model.generate_subTask(
        user=model.User(
            name=selectUser.name,
            workLifeRatio=selectUser.work_life_ratio,
            job=selectUser.job,
            gender=selectUser.gender,
            furtherDetails=selectUser.further_details,
            preferTask=selectUser.prefer_task,
            age=selectUser.age
        ),
        task=model.Task(
            title=create_task_req.title,
            body=create_task_req.body,
            start_time=create_task_req.start,
            end_time=create_task_req.end,
            category="time"
        )
    )
    print(subtasks)
    aiTask: AiSubTask = json.loads(subtasks)

    aiType = model.classification_task(selectUser, aiTask, "")

    create_task_req.type = aiType

    insertTask = task_schema.CreateTaskReq(
        type=aiType.type,
        title=aiType.title,
        body=aiType.body,
        start=aiType.start,
        end=aiType.end,
    )
    new_task = task_crud.create_task(insertTask, int(authorization), db)

    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": {
            "task_id": new_task.id
        }
    }


class AiTask:
    title: str
    body: str
    start: int
    end: int
    category: str
    subTasks: list


class AiSubTask:
    title: str
    body: str
    start: int
    category: str


@app.get("")
async def get_task(req: task_schema.GetTaskReq = Depends(), db: Session = Depends(get_db)) -> Dict[str, Any]:
    list = task_crud.get_tasks(datetime.utcfromtimestamp(req.start), datetime.utcfromtimestamp(req.end), db)

    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": list.list
    }


@app.put("/{id}")
async def put_task(id: int, new_task: task_schema.NewTask, db: Session = Depends(get_db)) -> Dict[str, Any]:
    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": None
    }


@app.delete("/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    if not task_crud.delete_subtask(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 서브태스크입니다."
        )

    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": None
    }

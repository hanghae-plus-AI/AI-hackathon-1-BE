from datetime import datetime
import json
from typing import Dict, Any, Annotated

from task import task_schema, task_crud
from user import user_schema, user_crud, user_router
from models import User

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Header

from database import get_db
from ai import ai_model
from user.user_router import ResponseSchema

app = APIRouter(prefix="/task")


@app.post("")
async def post_task(
        create_task_req: task_schema.CreateTaskReq, db: Session = Depends(get_db),
        authorization: Annotated[str, Header()] = "1"
) -> Dict[str, Any]:
    selectUser: User = user_crud.get_user_by_autoincrement(int(authorization), db)
    print(selectUser)

    task = ai_model.generate_subTask(
        user=ai_model.User(
            name=selectUser.name,
            workLifeRatio=selectUser.work_life_ratio,
            job=selectUser.job,
            gender=selectUser.gender,
            furtherDetails=selectUser.further_details,
            preferTask=selectUser.prefer_task,
            age=selectUser.age
        ),
        task=ai_model.Task(
            title=create_task_req.title,
            body=create_task_req.body,
            start_time=create_task_req.start,
            end_time=create_task_req.end,
            category="time"
        )
    )

    ai_task: ai_model.AiTask = task

    new_task = task_crud.create_task(task_schema.NewTask(
        type="TASK",
        classify=ai_task.get("classify"),
        title=ai_task.get("title"),
        body=ai_task.get("body"),
        start=datetime.utcfromtimestamp(ai_task.get("start")),
        end=datetime.utcfromtimestamp(ai_task.get("end")),
    ), int(authorization), db)

    for sub_task in ai_task.get("subTasks"):
        task_crud.create_task(task_schema.NewTask(
        type="TASK",
        classify=ai_task.get("classify"),
        title=sub_task.get("title"),
        body=sub_task.get("body"),
        start=datetime.utcfromtimestamp(sub_task.get("start")),
        end=None
    ), int(authorization), db)


    return user_router.ResponseSchema(
        statusCode=200,
        message="API 호출 성공",
        data={"task_id": new_task.id}
    )


@app.get("")
async def get_task(req: task_schema.GetTaskReq = Depends(), db: Session = Depends(get_db)) -> Dict[str, Any]:
    list = task_crud.get_tasks(datetime.utcfromtimestamp(req.start), datetime.utcfromtimestamp(req.end), db)

    return user_router.ResponseSchema(
        statusCode=200,
        message="API 호출 성공",
        data=list
    )

    # return list


@app.put("/{id}")
async def put_task(id: int, new_task: task_schema.NewTask, db: Session = Depends(get_db)) -> Dict[str, Any]:

    return user_router.ResponseSchema(
        statusCode=200,
        message="API 호출 성공",
        data=None
    )



@app.delete("/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:

    if not task_crud.delete_task(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 서브태스크입니다."
        )

    return user_router.ResponseSchema(
        statusCode=200,
        message="API 호출 성공",
        data=None
    )



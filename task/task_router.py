from datetime import datetime
from typing import Dict, Any, Annotated
from task import task_schema, task_crud

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Header

from database import get_db

app = APIRouter(prefix="/task")


@app.post("")
async def post_task(
        create_task_req: task_schema.CreateTaskReq, db: Session = Depends(get_db),
        authorization: Annotated[str | None, Header()] = "1"
) -> Dict[str, Any]:
    new_task = task_crud.create_task(create_task_req, authorization, db)



    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": {
            "task_id": new_task.id
        }
    }




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

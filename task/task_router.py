from typing import Dict, Any
from task import task_schema, task_crud

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from database import get_db

app = APIRouter(prefix="/task")

@app.post("")
async def post_task(new_task: task_schema.NewTask, db: Session = Depends(get_db)) -> Dict[str, Any]:
    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": None
    }

@app.get("")
async def get_subtask(db: Session = Depends(get_db)) -> Dict[str, Any]:
    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": None
    }


@app.put("/{id}")
async def put_task(id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": None
    }

@app.delete("/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    # if not task_crud.delete_subtask(id, db):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="존재하지 않는 서브태스크입니다."
    #     )

    return {
        "code": 200,
        "message": "API 호출 성공",
        "data": None
    }



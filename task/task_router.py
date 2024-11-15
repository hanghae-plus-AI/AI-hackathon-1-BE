from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from typing import Dict, Any
import task_crud

router = APIRouter(prefix="/subtask")

@router.delete("/{id}")
async def delete_subtask(id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    if not task_crud.delete_subtask(id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 서브태스크입니다."
        )
    
    return {
        "code": "OK-200",
        "message": "API 호출 성공",
        "data": None
    }
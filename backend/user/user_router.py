from sqlalchemy.orm import Session
from database import get_db

from fastapi import APIRouter, Depends, HTTPException, status

from user import user_schema, user_crud

app = APIRouter(
    prefix="/user"
)

@app.post(path="/signup")
async def signup(new_user: user_schema.NewUser, db: Session=Depends(get_db)):
    # 기존 회원과 id가 겹치는지 확인
    user = user_crud.get_user(new_user.user_id, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 id입니다.")
    
    # 회원가입
    user_crud.create_user(new_user, db)

    return HTTPException(status_code=status.HTTP_200_OK, detail="회원가입 완료")
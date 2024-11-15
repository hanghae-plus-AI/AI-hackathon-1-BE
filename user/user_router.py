from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

from user import user_schema, user_crud
from database import get_db

app = APIRouter(
    prefix="/user"
)

T = TypeVar('T')

class ResponseSchema(BaseModel, Generic[T]):
    statusCode: int
    message: str
    data: Optional[T] = None

@app.post(path="/signup")
async def signup(new_user: user_schema.NewUser, db: Session=Depends(get_db)):
    # 기존 회원과 id가 겹치는지 확인
    user = user_crud.get_user(new_user.user_id, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 id입니다.")
    
    # 회원가입
    user_crud.create_user(new_user, db)

    return ResponseSchema(
        statusCode=200,
        message="회원 가입 완료",
        data=None
    )


@app.post(path="/login")
async def login(login_form: user_schema.LoginFormat, db: Session = Depends(get_db)):
    # 회원인지 확인
    user = user_crud.get_user(login_form.user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="존재하는 id가 아닙니다.")
    
    # 로그인
    varified_user = user_crud.verify_password(login_form.password, user.password)
    if not varified_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="올바르지 않은 password입니다.")

    return ResponseSchema(
        statusCode=200,
        message="로그인 완료",
        data={"id": user.id}
    )

    
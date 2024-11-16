from pydantic import BaseModel, model_validator, field_validator
from datetime import datetime
from typing import Optional
from fastapi import HTTPException


class NewTask(BaseModel):
    type: str
    title: str
    body: Optional[str] = None
    start: datetime
    end: Optional[datetime] = None

    @model_validator(mode="before")
    def check_empty(cls, input):
        required_fields = ['type', 'content', 'start']
        for field in required_fields:
            value = input.get(field)
            if not value:
                raise HTTPException(status_code=422, detail="필수 항목을 모두 입력해주세요.")
        return input

    @field_validator('type')
    def validate_type(cls, input):
        valid_types = ['TASK', 'SUBTASK']
        if input not in valid_types:
            raise HTTPException(status_code=422, detail="유효하지 않은 타입입니다.")
        return input


class UpdateTaskReq(BaseModel):
    id: int
    type: str
    title: str
    body: str
    start: int
    end: int


class CreateTaskReq(BaseModel):
    type: str
    title: str
    body: str
    start: int
    end: int


class GetTaskReq(BaseModel):
    start: int
    end: int


class NewTask(BaseModel):
    type: str
    title: str
    body: str
    start: int
    end: int


class NewTaskHistory(BaseModel):
    id: int
    task_id: int
    type: str
    title: str
    body: str
    status: str
    start: datetime
    end: datetime
    created_at: datetime

    @field_validator('task_id', 'type', 'title', 'start', 'end')
    def check_empty(cls, input):
        if not input or (isinstance(input, str) and input.isspace()):
            raise HTTPException(status_code=422, detail="필수 항목을 모두 입력해주세요.")
        return input

    @field_validator('type')
    def validate_type(cls, input):
        valid_types = ['NORMAL', 'URGENT', 'DELAY']
        if input not in valid_types:
            raise HTTPException(status_code=422, detail="유효하지 않은 타입입니다.")
        return input

    class Config:
        from_attributes = True

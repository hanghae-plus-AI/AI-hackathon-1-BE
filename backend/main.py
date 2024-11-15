from fastapi import FastAPI

import models
from database import engine
models.Base.metadata.create_all(bind=engine)

from user import user_router

app = FastAPI()

app.include_router(user_router.app, tags=["user"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}
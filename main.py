from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
models.Base.metadata.create_all(bind=engine)

from user import user_router

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.app, tags=["user"])

@app.get("/")
def read_root():
    return {"message": "Hello World"}
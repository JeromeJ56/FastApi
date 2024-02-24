from fastapi import FastAPI,Response,status,HTTPException,Depends
from typing import Optional,List
from .import models,schemas,utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post,user


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


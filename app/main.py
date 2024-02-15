from fastapi import FastAPI,Response,status,HTTPException,Depends
# from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    # rating: Optional[int] = None

try:
    conn = psycopg2.connect(host="localhost",database="fastapi",user='jerome',password='pass,123',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection is succesfull!")
except Exception as error:
    print("connecting database failed!")
    print(f"Error: {error}")


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status":posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    """ Get all posts request """
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post : Post,db: Session = Depends(get_db)):
    """ Create post request """
    # cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title,content=post.content,published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id: int,db: Session = Depends(get_db)):
    """ Get post by id request """
    # cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id)))
    # post = cursor.fetchone()
    post =db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)  
def delete_post(id: int,db: Session = Depends(get_db)):
    """ Delete post request """
    # cursor.execute("DELETE FROM posts WHERE id = %s returning * ",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
@app.put("/posts/{id}")
def update_post(id:int,updated_post:Post,db: Session = Depends(get_db)):
    """ Update post request """
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published=%s WHERE id=%s RETURNING *",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data":post_query.first()}
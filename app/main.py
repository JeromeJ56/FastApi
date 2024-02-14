from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating: Optional[int] = None

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

@app.get("/posts")
def get_post():
    """ Get all posts request """
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    """ Create post request """
    cursor.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    """ Get post by id request """
    cursor.execute("SELECT * FROM posts WHERE id=%s",(str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)  
def delete_post(id: int):
    """ Delete post request """
    cursor.execute("DELETE FROM posts WHERE id = %s returning * ",(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    """ Update post request """
    cursor.execute("UPDATE posts SET title = %s, content = %s, published=%s WHERE id=%s RETURNING *",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    return {"data":updated_post}
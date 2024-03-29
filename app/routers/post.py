from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import Optional,List
from ..import models,schemas
from ..database import engine,get_db
from sqlalchemy.orm import Session
from .. import oauth2

router = APIRouter(prefix="/posts",tags=["Posts"])


@router.get("/",response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    """ Get all posts request """
    print(current_user.email)
    posts = db.query(models.Post).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post : schemas.PostCreate,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    """ Create post request """
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id: int,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    """ Get post by id request """
    post =db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id : {id} not found")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)  
def delete_post(id: int,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    """ Delete post request """
    post_query = db.query(models.Post).filter(models.Post.id==id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    """ Update post request """
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
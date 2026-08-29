from fastapi import status, APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy import func
from .. import schemas, models
from ..database import get_db
from . oauth2 import get_current_user
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, is_published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.is_published))
    # new_post = cursor.fetchone()
    # connection.commit()
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user = Depends(get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post)
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {"data": posts}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id:{id} doesnt exist.")
    # if (current_user.id != post.owner_id):
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    return post

@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db:Session=Depends(get_db), current_user = Depends(get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, is_published=%s WHERE id=%s RETURNING *""", (post.title, post.content, post.is_published, id,))
    # updated_post = cursor.fetchone()
    # connection.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id:{id} doesnt exist.")
    if (current_user.id != updated_post.owner_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    post_query.update(post.model_dump())
    db.commit()
    db.refresh(updated_post)
    return updated_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id, ))
    # cursor.fetchone()
    # connection.commit()
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_be_deleted = delete_query.first()
    if post_to_be_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with given id:{id} doesnt exist.")
    if (current_user.id != post_to_be_deleted.owner_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    delete_query.delete()
    db.commit()


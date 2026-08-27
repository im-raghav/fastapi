from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from .oauth2 import get_current_user

router = APIRouter(tags=['Votes'], prefix='/vote')

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with id: {current_user.id} has already voted for post with id: {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {current_user.id} has not voted for post with id: {vote.post_id}")
        vote_query.delete()
        db.commit()
        return {"message": "vote removed succesfully"}

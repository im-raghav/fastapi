from fastapi import status, APIRouter, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. database import get_db
from .. import schemas, models, utils
from . import oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credentials")

    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    return {"access_token": access_token, "token_type":"bearer"}




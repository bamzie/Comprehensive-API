from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.ORM.database import get_db
import schema
import app.ORM.modelsORM as modelsORM
from utils import verify
from  authToken import create_access_token 


 
##################################################
##################################################
# 
# Project for the User interface
# Path operations for logging/authenticating Users
#
##################################################
##################################################

router = APIRouter(tags = ['Authentication'])


# login endpoit
@router.post('/login', response_model= schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):


    # OAuth2 returns username (not email!!), password as a dict
    # that is why user_credentials.username
    # look for the email in database and set to user if found
    used = db.query(modelsORM.User).filter(
                modelsORM.User.email == user_credentials.username).first()
    # raise exception if not found
    if not used:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                    detail= f"Invalid Credentials") 

    # verify password by verif() in auth.py                   
    if not verify(user_credentials.password, used.password): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail= f"Invalid Credentials")

    #create a token
    # and return token
    access_token = create_access_token(data = {"user_id": used.id})

    return {"access_token": access_token, "token_type": "bearer"}


from typing import List
from schema import UserCreates, UserOutput
import modelsORM, utils
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from database import get_db


##################################################
##################################################
# 
# Project for the User interface
# Path operations for working with users
#
##################################################
##################################################

#router object
router = APIRouter(
    prefix="/users",
    # This groups our routers path operations in localhost:8000/docs 
    # as categories. This is included in FastAPI
    tags = ['Users']
) 


##################################################
# Create User
##################################################

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= UserOutput)
def create_usert(user: UserCreates, db: Session = Depends(get_db)):

    # Hash the password from user.password
    hashed_passwowrd = utils.hash(user.password)
    user.password = hashed_passwowrd

    #Create new user and send to backend
    new_user = modelsORM.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 



##################################################
# Get User
##################################################


@router.get('/{id}', response_model=UserOutput)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(modelsORM.User).filter(modelsORM.User.id == id).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id: {id} does not exists")
    return user
from datetime import datetime
from typing import Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr, conint


# This is reffered to as the schema

# User sending data to backend
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# We inherit the PostBase class by passing 
# in PostBase
# sending to the backen
class PostCreate(PostBase): 
    pass

# Backend sendind data back to user (front end)
class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:   
        orm_mode = True

# Us sending data to the user
# We inherit the PostBase model
# since we are returning the same values
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    #this will return a pydantic model type
    owner: UserOutput

    # this class allows us to return the values as 
    # a dict
    class Config:   
        orm_mode = True

# backends sends data in a dict() and value
# so we send setup our PostOut schema to 
# to send as a dict() and value (Post & votes)
class PostOut(BaseModel):
    Post: Post
    votes: int

class UserCreates(BaseModel):
    email: EmailStr
    password: str


# Backend sendind data back to user (front end)
class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:   
        orm_mode = True


# Login(frontend) sending valid data to backend
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Access token sent by the frontend to the backend
class Token(BaseModel):
    access_token: str
    token_type: str

# The data we embedded to our access token sent by the backend
# to this frontend schema
class TokenData(BaseModel):
    id: Optional[str] = None

# This will be the user (frontend) sending a
# vote to the backend
class Vote(BaseModel):
    post_id: int
    # problem: this allows negative values
    # setup resitriction
    dir: conint(le=1)
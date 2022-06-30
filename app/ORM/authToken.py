from http.client import HTTPException
from lib2to3.pgen2.tokenize import TokenError
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schema import TokenData
from fastapi.security import OAuth2PasswordBearer
import database
from sqlalchemy.orm import Session
import modelsORM
from config import settings

##################################################
##################################################
# 
# Creates our JWT Token that will be provide to 
# the front end. Front end will always send the token
# with the payload so that the backend verifies the 
# token. Backend holds not token.
#
##################################################
##################################################
 
# this will be our login endpoint given us the access token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY
# Algorithm
# Expiration time

# just provide some kind of string in .env file
# using .env file so that our backend updates accordingly
# to a new machine (look at database.py for more explanation)
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):

    # we copy so we dont actually change the original data (payload)
    to_encode = data.copy()

    # create the expiration field
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # update the dict to add expiration time so jwt will tell us when it will expire
    to_encode.update({"exp": expire})

    # this create the jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_access_token(token: str, credentials_exception): 

    # incase any line of code might error out
    try:
        # we decode token and store to payload
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])

        # we extract the field we put in which is users_id in auth.py
        id: str = payload.get("user_id")

        # if no id raise exception
        if id is None: 
            # whatever excpetion we pass in the argue
            raise credentials_exception

        #set the extracted id to the TokenData Schema
        token_data = TokenData(id = id)

    #
    except JWTError: 
        raise credentials_exception
    return token_data


# we pass this as a dependencies to any path operations
# and it will take the token from the request automatically (oauth2-scheme)
# then call the verify_access_token() and extract the id
# Finally automatically fetch the user from the database and
# add it as a parameter to our path operations function
# this fetches the user from the database
def get_current_user(token: str = Depends(oauth2_scheme),
                    db: Session = Depends(database.get_db)):

    # so when there is some type of issue with the credentials token
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                    detail = f"Could not validate credentials",
                                    headers = {"WWW-Authenticate": "Bearer"})


    token = verify_access_token(token, credentials_exception)

    # this fetches the user from the database
    user = db.query(modelsORM.User).filter(modelsORM.User.id == token.id).first()

    # return a call to our verify_access_token()
    return user


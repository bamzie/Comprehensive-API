
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
 
import routers.post as post
import routers.users as users  
import routers.auth as auth
import routers.vote as vote
 
  
# print(settings.database_username)

# This is the code the creates our table
# this tells sqlalchemy to run our create statements
# The modelsORM allows us to make queries to it.
# -------------------------------
# modelsORM.Base.metadata.create_all(bind=engine)
# -------------------------------
# no longer need this because we connected alembic 
# to do this

app = FastAPI(); 

# Before this my local machine was the only one able to 
# communicate through my api
# this allows other web browser domains to 
# use our api
# * means all web browsers
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    # who can communicate to our api
    allow_origins=origins,
    allow_credentials=True,
    # allow only specific http methods (ex: not want put
    # or post methods only get)
    # for now we allow all (*)
    allow_methods=["*"],
    # allow specific headers
    allow_headers=["*"],
)


@app.get('/')
def get_hello():
    return {"message": "Hi bamz"}
# When we get a HTTP request
# we go to our app reference and look at all the routes
# from out router folder
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)




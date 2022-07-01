from fastapi import Depends, HTTPException, status, Response, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import modelsORM
from database import engine, get_db
from schema import PostCreate, Post, PostOut
import authToken


##################################################
##################################################
#
# Path Operatiions for Handling CRUD operations 
# for Post
#
##################################################
##################################################



# routers object 
router = APIRouter(
    prefix= "/posts",
    # This groups our routers path operations in localhost:8000/docs 
    # as categories. this is included in FastAPI
    tags = ['Posts'] 
)

##################################################
# GET All Post
##################################################
@router.get("/", response_model= List[PostOut])
# Whenever we want to perform a database operation we must
# pass as parameter Depends(get_db) (e.i. GET, PUT, etc)
# limit: limited of post to return
# skip: skip the first number of queries
# search: search a title of posts
def get_posts(db: Session = Depends(get_db),
            current_user: int = Depends(authToken.get_current_user),
            limit: int = 10, skip: int = 0, search: Optional[str] =""):

    # NO SQL, we tap into the database oject (db)
    # we access the database object, 
    # we use the query method to do a query
    # go to our modelsORM and select Post
    # and we select all

    #---------------------------
    # This code allows us to retrieve all of the owners post
    # not eveyones posts in the database. 
    # post = db.query(modelsORM.Post).filter(
    #                 modelsORM.Post.owner_id == current_user.id).all()
    #---------------------------


    #---------------------------
    # For this case, we want all posts
    #post = db.query(modelsORM.Post).all()
    #---------------------------

    # user retreives the set limited amount, skip, 
    # and search of post
    #--------------------------
    # post = db.query(modelsORM.Post).filter(modelsORM.Post.title.contains(search)).limit(
    #                limit).offset(skip).all()
    #--------------------------


    # we are setting up a join query
    # so that we can return the number of likes/votes
    # that were done on a posts
    #__________________________________________
    # SELECT posts.*, COUNT(votes.post_id) as votes FROM posts 
    # LEFT JOIN votes ON posts.id = votes.post_id 
    # group by posts.id; 
    # ^^ what we are doin g^^
    # func.count() does the COUNT() in SQL
    #label() renames your column in SQL
    # NOTE: SQLalchemy join() is defualted as an outer join
    post = db.query(modelsORM.Post, func.count(modelsORM.Vote.post_id).label("votes")).join(modelsORM.Vote, modelsORM.Vote.post_id == modelsORM.Post.id,
                       isouter = True ).group_by(modelsORM.Post.id).filter(modelsORM.Post.title.contains(search)).limit(
                    limit).offset(skip).all()
 
    return post


##################################################
# CREATE Post 
##################################################

# this is called a path parameter
# uses the id that has been passes to url
# the response_model returns what we decide to return to the user 
# in this case our Post model
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)

# Since the user needs to be logged in to create a post 
# we add an extra dependecies   get_current_user   . So anytime any one 
# wants to access a resource that requires them to be logged in 
# the must provide a access token that is not expired. 
def create_post(post: PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(authToken.get_current_user)):

    # current_user provides us with the users info 
    # so we can addd owner_id from current_user. 
    # Look at auth.py

    ## This is to tedious if we have 50 attributes
    #      new_post = modelsORM.Post(title = post.title, content = post.content, published = post.published)
    # This unpacks our model FrontEndPost 
    # adn automatically sets all the required fields
    new_post = modelsORM.Post(owner_id = current_user.id, **post.dict())
    # add this newly created post to database
    db.add(new_post)
    # then commit this addition (save)
    db.commit()
    # this retrieves the new post we created
    # stores it in new post again
    db.refresh(new_post)


    return new_post



##################################################
# GET Post with ID
##################################################

@router.get("/{id}", response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db),
            current_user: int = Depends(authToken.get_current_user)):

    # get one post and all its info 
    # using Post as response models
    # post = db.query(modelsORM.Post).filter(modelsORM.Post.id == id).first()

    # get one post and all its info with the vote variable attached
    # using PostOut as response model
    post = db.query(modelsORM.Post, func.count(modelsORM.Vote.post_id).label("votes")).join(modelsORM.Vote, modelsORM.Vote.post_id == modelsORM.Post.id,
                       isouter = True ).group_by(modelsORM.Post.id).filter(modelsORM.Post.id == id).first()
    if not post:
        # status.HTTP... gives us different statuses
        # detail returns a message to the user
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with ID {id} was not found")

    #-------------------
    # this piece of code allows us to retrieve only the signed-in
    # user posts. Not anyones post
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not authorized to perform requested action")
    #-------------------
    return post


##################################################
# DELETE Post
##################################################


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)

def delete_posts(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(authToken.get_current_user)):

    # We find the post to delete
    post_query = db.query(modelsORM.Post).filter(modelsORM.Post.id == id)

    # pull ou the first post that matches
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                             detail = f"post with id: {id} does not exist")
     
    # We check if its the correct owner of the post. If not throw an error and do not delete 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    # We delete the post
    # Read about the synchronize session
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)

##################################################
# Update Post
##################################################



@router.put("/{id}", response_model=Post)

def update_post(id: int, updated_post: PostCreate, db: Session= Depends(get_db),
                current_user: int = Depends(authToken.get_current_user)):

    # This finds our post by id using filter
    post_query = db.query(modelsORM.Post).filter(modelsORM.Post.id == id)

    # We grab the first post that matches our id
    # and set it to post to check if it exists
    post = post_query.first()

    # If it does not exist throw error
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")


    # If it exist we update the post
    post_query.update(updated_post.dict(), synchronize_session=False)
    # As always commit
    db.commit()

    return post_query.first()


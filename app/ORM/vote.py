from fastapi import Depends, HTTPException, status, APIRouter
from schema import Vote
import database, modelsORM, authToken
from sqlalchemy.orm import Session


##################################################
##################################################
# 
# Path operations for working with votes
#
##################################################
##################################################

#setup router and path
router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)


##################################################
# Vote a post
##################################################

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(database.get_db), 
        current_user: int = Depends(authToken.get_current_user)):

    # first we check if the post exists or not
    post = db.query(modelsORM.Post).filter(modelsORM.Post.id == vote.post_id).first()
    # if post DNE then send 404 
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post {vote.post_id} does not exists")
    

    # want to creat a vote and we check if a vote already exist
    # by checking on post id and user id
    # Essentially checks if this user already voted this post
    vote_query = db.query(modelsORM.Vote).filter(modelsORM.Vote.post_id == vote.post_id, 
            modelsORM.Vote.user_id == current_user.id)
    
    # if the user wants to like/vote a post but we already found
    # a vote by user, then found_vote wont allow him to vote againe
    found_vote = vote_query.first()

    # direction = 1, wants to create a vote 
    if(vote.dir == 1):
        # if found_vote = True therefore user has already voted
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        #  not found then like/vote for the post                            
        new_vote = modelsORM.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    # if direction of 0, means they want to delete a pre-existing vote    
    else: 
        # we cant delete a vote that doesnt exist
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does note exist" )
        # if we did find a vote, delete it
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}


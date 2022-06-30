from cgi import test
from fastapi import FastAPI, HTTPException, status, Response
from psycopg2 import connect
from app.pythonWithSQL.models import Post
from random import randrange
import app.pythonWithSQL.dbConn
from app.pythonWithSQL.dbConn import cursor, conn

app.pythonWithSQL = FastAPI(); 


my_posts = [{"title": "title of post 1", 
            "content": "content of post 1",
            "id": 1}, 
            {"title": "Fav artist", 
            "content": "lil wayne", 
            "id":2}]

def find_post(id): 
    for p in my_posts: 
        if p["id"] == id: 
            return p


def find_index_posts(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id: 
            return i

##################################################
# GET post
##################################################

# Order matter with PATH parameters (GET, PUT,...)
# Make sure you have them properly ordered
# request comes in with a Get method looking
# for url: "/" 
# This is a decorator
# get() is the method
# "/" is the root path. The path after your domain URL
@app.pythonWithSQL.get("/posts")

# Async means we will perform asyncronous task
# the function itself is arbitrary. However be desceptive
async def get_posts(): 
    # This will have all the credentials for when you login

    # execute() is where you enter your SQL statement
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return{"data": posts}



##################################################
# CREATE Post
##################################################

# statust code will return a 201 created with successful
@app.pythonWithSQL.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post): 
    # #converting to dictionary
    # post_dict = post.dict()
    # # set id to a randome number using randrange
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)

    # Thes %s are the variables, respectively. 
    # (e.g. (%s, %s, %s)-> (post.title, post.content, post.published))
    # Must be enter in order, respectively
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                (post.title, post.content, post.published))
    # The fetch comes from the RETURNING * and we only fetch one
    #the one we created
    new_post = cursor.fetchone()

    # to commit and finalize the posts
    conn.commit()
    return {"data": new_post} 


 
##################################################
# GET Post with ID
##################################################

# this is called a path parameter
#uses the id that has been passes to url
@app.pythonWithSQL.get("/posts/{id}")
def get_post(id: int):

    #Same as before but new SQL lines for getting one post 
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    #If id does not exists, response, returns a status code of 404
    if not post:
        # status.HTTP... gives us different statuses
        # detail returns a message to the user
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with ID {id} was not found")
    return{"post_detail":post}



##################################################
# DELETE Post
##################################################


@app.pythonWithSQL.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)

def delete_posts(id: int):
    # deleting posts
    # find the index in the array that has required ID

    # Same as before
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_posts = cursor.fetchone()
    # we must commit to delete
    conn.commit()

    if deleted_posts == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")

    return Response(status_code = status.HTTP_204_NO_CONTENT)


##################################################
# Update Post
##################################################



@app.pythonWithSQL.put("/posts/{id}")

def update_post(id: int, post: Post):
    # SQL commands to update posts
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id: {id} does not exist")
 
    return {"data": updated_post}  

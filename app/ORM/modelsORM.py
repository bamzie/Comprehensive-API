from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from app.ORM.database import Base
from sqlalchemy.orm import relationship


# We are programming the SQL table in python
class Post(Base): 
    # Table name
    __tablename__ = "posts"

    #Columns being created in the table
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable = False, server_default = 'True')
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default = text('now()'))

    # This will be the foreign key and the relationship
    # that will bind the posts and users table 
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                        nullable = False)

    # this will create another property for our post (dict)
    # it will return a owner property and figure out
    # the relationship to user
    # and fetch the user for use
    owner = relationship("User")

# users tables
class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable= False, unique=True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default = text('now()'))
    phone_number = Column(String)

# This table will be a Composite key table
# for votes 
class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Connects to our database
# Right now this is running on our localmachine
# What the url is looking for: 
# 'postgresql://<username>:<password>@ip-address:<port #>/<hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# However in production we are not running in our local maachine.
# It may not be running in the machine its depoloyed on, it can be
# running on a completely different system.
# So we need a solution where the code can update to its
# enviroment. ENVIROMENT VARIABLE!!


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush =False, bind =  engine)

Base = declarative_base()

# Dependency
# This function creates a session towards our database
# for every request towards our api endpoint. this closes
# out once we are done with the request. 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
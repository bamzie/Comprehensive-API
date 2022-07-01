from pydantic import BaseSettings

 ############################################
 # This will setup our database enviroment
 # it will update accordingly to machine 
 ############################################

# pydantic will read the enviroment variable as a string


# This will provide all the enviroment variables
# that need to be set for the database connection
# reference database.py for why we do this
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str 
    access_token_expire_minutes: int

    # pydantic will import our .env file 
    # and fill-in our required variables
    class Config: 
        env_file = ".env"
        env_file_encoding = 'utf-8'
      
settings = Settings()     
 

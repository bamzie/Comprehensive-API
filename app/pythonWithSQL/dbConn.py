import psycopg2
from psycopg2.extras import RealDictCursor
import time

# This connects to the database using raw SQL
# if wanting to connect through enviroment variable
# import config (make sure to move config file into folder 
# and .env file into folder)
# and change variales in pycog2.connect()
#  ex: host = config.settings.database_hostname...
while True: 

    try: 
        conn = psycopg2.connect(host = 'localhost', database = 'comprehApi', user = 'postgres', 
                                password = 'tygh', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error: 
        print("Connection to database failed")
        print("Error: ", error) 
        time.sleep(2)
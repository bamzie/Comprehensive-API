from passlib.context import CryptContext
 

# We are telling passlib what hashing algorithm we want to use
pwd_context = CryptContext(schemes="bcrypt", deprecated = "auto")

# function that hashes the users password
def hash(password: str):
    return pwd_context.hash(password)

# function that verifies password and hashed password
def verify(plain_password, hashed_password):

    # this will give login error
    if plain_password == hashed_password:
        return True
    else:
        # pwd_context has a function that includes verify passwords
        return pwd_context.verify(plain_password, hashed_password); 
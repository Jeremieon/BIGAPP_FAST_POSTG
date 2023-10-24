#import module to encrypt contexts
from passlib.context import CryptContext

#encrypt passwords using bcrypt algo
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#check if the input password is correct
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

#generated a password hash using bcrypt
def get_password_hash(password):
    return pwd_context.hash(password)
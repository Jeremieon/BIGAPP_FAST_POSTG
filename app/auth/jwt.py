from datetime import datetime,timedelta
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.auth import schema
#from app import config

#define secret keys and algo
SECRET_KEY = "31df8a9d99142f097c48946d30dc87684acc9f06852517ddf7b2f77ba36d9eb4" #config.SECRET_KEY
ALGORITHM = "HS256" #config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#oauth format
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#token that will be created when i login
def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

#verify the user token
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        id: int = payload.get("id")
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email,id=id)
        return token_data
    except JWTError:
        raise credentials_exception

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)

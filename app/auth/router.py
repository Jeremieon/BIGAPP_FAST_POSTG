#import modeules and dependencies
from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import db
from app.user import hashing
from app.user.models import User
from .jwt import create_access_token
from .schema import Login
router = APIRouter(tags=["authentication"])

#request: OAuth2PasswordRequestForm = Depends()
#request:Login
@router.post('/login')
def login(request:Login, database: Session = Depends(db.get_db)):
    user = database.query(User).filter(User.email == request.username).first()
    id = user.id
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})
    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Password')
    
    #Generate JWT Token
    access_token = create_access_token(data={"id":id,"sub":user.email})

    return {"access_token": access_token, "token_type": "bearer"}
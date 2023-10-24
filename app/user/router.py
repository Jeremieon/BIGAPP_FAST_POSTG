#mport all required deps and modules
from typing import List

from fastapi import APIRouter, Depends,status,Response, HTTPException
from sqlalchemy.orm import Session
from app.auth.jwt import get_current_user
from app import db
from . import schema
from . import services
from . import validator

#create a router for the user app it will tag this section and append user endpoint to the uri
router = APIRouter(tags=['Users'], prefix='/user')


#create what happens when you hit the / endpoint i.e user endpoint
@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user_registration(request:schema.User,database:Session = Depends(db.get_db)):

    #check if user already exit using the verify function
    user = await validator.verify_email_exist(request.email,database)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    #if user doesnt exist create new user using function from services
    new_user = await services.new_user_register(request, database)
    return new_user

#router to get users from the data base /
@router.get('/',response_model=List[schema.DisplayUser])
async def get_all_users(database: Session = Depends(db.get_db),current_user: schema.User = Depends(get_current_user)):
    return await services.all_users(database)

@router.get('/{user_id}', response_model=schema.DisplayUser)
async def get_user_by_id(user_id: int, database: Session = Depends(db.get_db),current_user: schema.User = Depends(get_current_user)):
    return await services.get_user_by_id(user_id, database)

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user_by_id(user_id: int, database: Session = Depends(db.get_db),current_user: schema.User = Depends(get_current_user)):
    return await services.delete_user_by_id(user_id, database)
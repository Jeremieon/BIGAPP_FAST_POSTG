from fastapi import APIRouter,Depends, status,Response
from sqlalchemy.orm import Session
from . import services
from app.auth.jwt import get_current_user
from app import db
from app.user.schema import User
from . import schema

router = APIRouter(tags=['Cart'], prefix='/cart')

@router.get('/add', status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(product_id: int,
                              database: Session = Depends(db.get_db),current_user: User = Depends(get_current_user)):
    result = await services.add_to_cart(product_id, database,current_user)
    return result

@router.get('/', response_model=schema.ShowCart)
async def get_all_cart_items(current_user: User = Depends(get_current_user),database: Session = Depends(db.get_db)):
    result = await services.get_all_items(database,current_user)
    return result

@router.delete('/{cart_item_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def remove_cart_item_by_id(cart_item_id: int,
                                 database: Session = Depends(db.get_db),current_user: User = Depends(get_current_user)):
    await services.remove_cart_item(cart_item_id, database,current_user)
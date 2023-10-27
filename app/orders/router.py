from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.auth.jwt import get_current_user
from app import db
from app.orders.services import initiate_order, get_order_listing
from app.user.schema import User
from .schema import ShowOrder

router = APIRouter(
    tags=['Orders'],
    prefix='/orders'
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowOrder)
async def initiate_order_processing(database: Session = Depends(db.get_db),current_user: User = Depends(get_current_user)):
    result = await initiate_order(database)
    return result

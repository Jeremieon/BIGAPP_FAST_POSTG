from typing import List
from fastapi import APIRouter,Depends,status,Response,HTTPException,File,UploadFile,Form
from sqlalchemy.orm import Session
from io import BytesIO
from app import db
from . import schema
from . import services
from . import validator

router = APIRouter(
    tags=['Products'],
    prefix='/products'
)

@router.post('/category', status_code=status.HTTP_201_CREATED)
async def create_category(text_data: str = Form(...), database: Session = Depends(db.get_db),images: UploadFile = File(...)):
    image_upload_dir = "images/category_images"
    image_url = await services.save_image(images, image_upload_dir)
    category_data = {}
    category_data["name"] = text_data
    category_data["image_url"] = image_url
    new_category = await services.create_new_category(category_data,database)
    return {"category": new_category}


@router.get('/category', response_model=List[schema.ListCategory])
async def get_all_categories(database: Session = Depends(db.get_db)):
    return await services.get_all_categories(database)
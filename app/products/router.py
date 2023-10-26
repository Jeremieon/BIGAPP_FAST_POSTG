from typing import List,Dict,AnyStr,Any
from fastapi import APIRouter,Depends,status,Response,HTTPException,File,UploadFile,Form,Request
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


@router.get('/category/{category_id}',response_model=schema.ListCategory)
async def get_category_by_id(category_id : int,database: Session = Depends(db.get_db)):
    return await services.get_category_by_id(category_id,database)

@router.delete('/category/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_category_by_id(category_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_category_by_id(category_id, database)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(
    name: str = Form(...),
    quantity: int = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
    category_id: int = Form(...),
    database: Session = Depends(db.get_db)):
    # Parse the JSON data from the request body
    # data = await request.json()
    category = await validator.verify_category_exist(category_id, database)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="You have provided invalid category id.",
        )
    
    image_upload_dir = "images/products_images"
    image_url = await services.save_image(image, image_upload_dir)
    request_data = {}
    request_data["name"] = name
    request_data["quantity"] = quantity
    request_data["description"] = description
    request_data["price"] = price
    request_data["image_url"] = image_url
    request_data["category_id"] = category_id
    product = await services.create_new_product(request_data, database)
    return product

@router.get('/', response_model=List[schema.ProductListing])
async def get_all_products(database: Session = Depends(db.get_db)):
    return await services.get_all_products(database)

@router.get('/{product_id}',response_model=schema.ProductListing)
async def get_product_by_id(product_id : int,database: Session = Depends(db.get_db)):
    return await services.get_product_by_id(product_id,database)

@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_product_by_id(product_id: int, database: Session = Depends(db.get_db)):
    return await services.delete_product_by_id(product_id, database)


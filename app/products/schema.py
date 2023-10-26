from pydantic import BaseModel, constr
from fastapi import UploadFile

class Category(BaseModel):
    name: constr(min_length=2, max_length=50)
    image_url:str
    
class ListCategory(BaseModel):
    id: int
    name: str
    image_url:str

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    quantity: int
    description: str
    price: float
    image_url: UploadFile

    class Config:
        from_attributes = True

class Product(ProductBase):
    category_id: int

class ProductListing(ProductBase):
    category: ListCategory

    class Config:
        from_attributes = True
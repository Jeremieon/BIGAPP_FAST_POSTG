from . import models
from typing import List
from fastapi import HTTPException,status,FastAPI,UploadFile
from PIL import Image
from io import BytesIO
from pathlib import Path
import os


async def save_image(image,image_upload_dir,max_width=300, max_height=300):
    # Ensure the upload directory exists
    os.makedirs(image_upload_dir, exist_ok=True)
    #path where the image should be saved
    image_path = os.path.join(image_upload_dir, image.filename)

    #Open the file and write the image data
    with open(image_path, "wb") as image_file:
        image_file.write(image.file.read())
    #resize image
    with Image.open(image_path) as img:
        width, height = img.size

        # Check if the image needs to be resized
        if width > max_width or height > max_height:
            # Calculate the new dimensions while maintaining aspect ratio
            ratio = min(max_width / width, max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)

            # Resize the image
            img = img.resize((new_width, new_height))

            # Save the resized image
            img.save(image_path)
    # with Image.open(image_path) as img:
    #     img.thumbnail((300, 300))
    #     img.save(image_path)
    return image_path 


async def create_new_category(category_data,database) -> models.Categories:
    new_category = models.Categories(**category_data)
    database.add(new_category)
    database.commit()
    database.refresh(new_category)

    return new_category


async def get_all_categories(database) -> List[models.Categories]:
    categories = database.query(models.Categories).all()
    return categories

async def get_category_by_id(category_id, database):
    category_info = database.query(models.Categories).get(category_id)
    if not category_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
    return category_info

async def delete_category_by_id(category_id, database):
    database.query(models.Categories).filter(models.Categories.id == category_id).delete()
    database.commit()
    return {"File Status" : f"category with category id :{category_id} has been deleted"}

async def create_new_product(request_data, database) -> models.Product:
    new_product = models.Product(name=request_data.get('name'), quantity=request_data.get("quantity"),
                                 description=request_data.get("description"), price=request_data.get("price"),
                                 image_url=request_data.get("image_url"),
                                 category_id=request_data.get("category_id"))
    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product

async def get_all_products(database) -> List[models.Product]:
    products = database.query(models.Product).all()
    return products

async def get_product_by_id(product_id, database):
    product_info = database.query(models.Product).get(product_id)
    if not product_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
    return product_info

async def delete_product_by_id(product_id, database):
    database.query(models.Product).filter(models.Product.id == product_id).delete()
    database.commit()

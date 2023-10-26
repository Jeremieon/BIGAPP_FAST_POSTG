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
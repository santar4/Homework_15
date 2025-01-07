import io

from PIL import Image
from fastapi import UploadFile, HTTPException
import os

UPLOAD_IMAGE_DIR = "./upload_images"
async def save_image(file: UploadFile):
    os.makedirs(UPLOAD_IMAGE_DIR, exist_ok=True)
    filename = f"Santar4_Gallery{file.filename}"
    file_path = os.path.join(UPLOAD_IMAGE_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, "path": file_path}



def optimaze_image(image_data: bytes) -> bytes:
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail((1024, 1024))
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format=img.format)
        return img_byte_array.getvalue()

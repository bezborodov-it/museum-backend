import os
import shutil
from datetime import datetime

from fastapi import UploadFile, HTTPException
from api.configuration.config import settings


def save_image(file: UploadFile) -> str:
    dir = os.path.join(settings.STATIC_DIR, "images")

    if not os.path.exists(dir):
        os.makedirs(dir)

    current_date = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
    extension = file.filename.split(".")[-1]
    filename = f"{current_date}.{extension}"
    file_path = os.path.join(dir, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/static/images/{filename}"

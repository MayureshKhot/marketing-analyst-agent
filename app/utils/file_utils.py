import os
from fastapi import UploadFile

async def save_upload(file: UploadFile, folder: str = "data") -> str:
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, file.filename)
    contents = await file.read()
    with open(filepath, "wb") as f:
        f.write(contents)
    return filepath

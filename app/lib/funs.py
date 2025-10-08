import os
from uuid import uuid4

from fastapi import UploadFile
from isort import file

def create_dir_if_not_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def save_file(file, path: str):
    with open(path, "wb+") as file_object:
        file_object.write(file.read())
    return path

def delete_file(path: str):
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def generate_unique_filename(original_filename: str) -> str:
    return f"{uuid4().hex}_{original_filename}"

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1]

def save_image(image: UploadFile, upload_dir: str) -> str:
    create_dir_if_not_exists(upload_dir)
    filename = generate_unique_filename(image.filename)
    file_location = f"{upload_dir}{filename}"
    save_file(image.file, file_location)
    return file_location

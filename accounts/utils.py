import os
import random

from django.core.files.storage import default_storage
from django.conf import settings


def save_uploaded_file(instance, filename):
    upload_dir = settings.MEDIA_AVATARS

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_ext = filename.split('.')[-1]

    filename = str(random.randint(1000000000, 9999999999))
    filename += '.' + file_ext

    while os.path.exists(os.path.join(upload_dir, filename)):
        filename = str(random.randint(1000000000, 9999999999))
        filename += '.' + file_ext

    file_path = os.path.join(upload_dir, filename)

    with default_storage.open(file_path, 'wb') as destination:
        for chunk in instance.chunks():
            destination.write(chunk)

    return file_path


def check_uploaded_image(image):
    true_ext = {'jpg', 'jpeg', 'png'}

    if not image:
        error = 'Файл не выбран'
        return error

    image_ext = image.name.split('.')[-1]
    if image_ext not in true_ext:
        error = 'Файл должен быть .jpg, .jpeg или .png'
        return error

    if image.size > settings.MAX_IMAGE_SIZE * 1024 * 1024:
        error = f'Максимальный размер загружаемых фотографий не может превышать {settings.MAX_IMAGE_SIZE}MB'
        return error
    return
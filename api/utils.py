import uuid
import os
from django.core.exceptions import ValidationError


def image_validator(image):
    breakpoint()
    file_size = image.size
    limit_kb = 200
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit_kb)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('images/', filename)

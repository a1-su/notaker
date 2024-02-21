from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from io import BytesIO
from PIL import Image
from .utils import image_resize


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#
#     def __str__(self):
#         return f'{self.user.username} Profile'
#
#     def save(self, commit=True, *args, **kwargs):
#         if commit:
#             image_resize(self.image, 250, 250)
#             super().save(*args, **kwargs)

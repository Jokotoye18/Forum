from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

# class Profile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='profile_pics', default='')

#     def __str__(self):
#         return f'{self.user} profile pics'

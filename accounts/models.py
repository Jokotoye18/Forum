from django.db import models
from django.contrib.auth import get_user_model
from allauth.account.signals import user_signed_up
from imagekit.models import	ImageSpecField	
from pilkit.processors import ResizeToFill

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    image_thumbnail	= ImageSpecField(source='image', processors=[ResizeToFill(350, 400)], format='JPEG', options={'quality': 60})


    objects = models.Manager

    def __str__(self):
        return f'{self.user} pics'

def user_profile(request, user, **kwargs):
    if user_signed_up:
        Profile.objects.create(user=user)

user_signed_up.connect(receiver=user_profile, sender=get_user_model())
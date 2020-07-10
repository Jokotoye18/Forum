from hashlib import md5

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def gravatar_img(user, size=35):
    email = str(user.email.strip().lower()).encode('utf-8')
    email_hash = md5(email).hexdigest()
    url = f'{user.profile.image.url}'
    return url.format(email_hash, size)
    
import hashlib
from urllib.parse import urlencode

from django import template
from django.conf import settings

register = template.Library()

@register.filter
def gravatar(user, avatar_size):
    email = user.email.lower().encode('utf-8')
    default = 'mm'
    size = int(avatar_size)
    if size == 0:
        size = 64
    
    url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
        md5=hashlib.md5(email).hexdigest(),
        params=urlencode({'d': default, 's': str(size)})
    )
    return url
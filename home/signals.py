from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.core.cache import cache
from django.dispatch import receiver


@receiver(user_logged_in, sender=User)
def login_success(sender, request, user, **kwargs):
    ct = cache.get('count', 0, version=user.pk)
    newcount = ct + 1
    cache.set('count', newcount, 60*60*20, version=user.pk)
    print(user.pk)
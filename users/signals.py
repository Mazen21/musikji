
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Badge

def _init_badges():
    Badge.objects.all().delete()
    bdg = Badge(title_eng="Musikji Member", css_class="primary")
    bdg.save()

@receiver(post_save, sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender,instance,**kwargs):
    bdg=Badge()
    try:
        bdg = Badge.objects.get(title_eng='Musikji Member')
    except Badge.DoesNotExist:
        _init_badges()
        bdg = Badge.objects.get(title_eng='Musikji Member')
    instance.profile.badges.add(bdg)
    instance.profile.save()

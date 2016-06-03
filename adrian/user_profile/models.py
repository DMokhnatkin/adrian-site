__author__ = 'Dmitriy'

from django.contrib.auth.models import User
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class UserProfile(models.Model):
    avatar = ThumbnailerImageField(upload_to='media/images/avatars', default='media/images/avatars/none.png')
    use_contacts_as_main = models.BooleanField(default=False)
    extra_information = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(User)


class PhoneNumber(models.Model):
    val = models.CharField(max_length=20)
    user = models.ForeignKey(UserProfile)

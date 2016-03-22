__author__ = 'Dmitriy'

from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


class Slideshow(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Slide(models.Model):
    label = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=50, blank=True)
    image = ThumbnailerImageField(upload_to='media/images/slides')
    slideshow = models.ForeignKey(Slideshow)
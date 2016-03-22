__author__ = 'Dmitriy'

from django.contrib import admin
from slideshows import models


class SlideInLine(admin.StackedInline):
    extra = 1
    model = models.Slide


@admin.register(models.Slideshow)
class SlideShowAdmin(admin.ModelAdmin):
    inlines = [SlideInLine]
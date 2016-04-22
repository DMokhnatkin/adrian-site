__author__ = 'Dmitriy'
from store.catalog import models as StoreModels
from django.db import models
from store.catalog.models import FieldType
from django.dispatch import receiver
from django.db.models import signals


class FilterSetting(models.Model):
    fieldType = models.OneToOneField('store.FieldType')
    active = models.BooleanField(default=False)
    filter_type = models.CharField(max_length=20, choices=(
        ('range', 'range'),
        ('Multiple choice', 'MultipleChoice')
    ))

    def __str__(self):
        return self.fieldType.name

    def category(self):
        return self.fieldType.category

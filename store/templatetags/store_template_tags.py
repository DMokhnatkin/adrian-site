__author__ = 'Dmitriy'

from store import models as store_models
from django import template
from decimal import *


register = template.Library()

# Get all categories
@register.assignment_tag(name='get_categories')
def get_categories():
    return store_models.Category.objects.all()


@register.inclusion_tag('store/template_tags/print_price.html')
def print_price_link():
    price = store_models.Price.objects.get(pk=1)
    return {'price': price}


@register.simple_tag(name='price_url')
def price_url():
    price = store_models.Price.objects.get(pk=1)
    return price.file.url
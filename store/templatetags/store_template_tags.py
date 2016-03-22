__author__ = 'Dmitriy'

from store import models as store_models
from django import template


register = template.Library()

@register.inclusion_tag('store/template_tags/show_categories.html')
def show_categories():
    categories = store_models.Category.objects.all()
    if categories:
        return {'categories': categories}
    else:
        return {'categories': None}


@register.inclusion_tag('store/template_tags/print_price.html')
def print_price_link():
    price = store_models.Price.objects.get(pk=1)
    return {'price': price}


@register.simple_tag(name='price_url')
def price_url():
    price = store_models.Price.objects.get(pk=1)
    return price.file.url
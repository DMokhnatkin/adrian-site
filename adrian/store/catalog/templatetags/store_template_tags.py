__author__ = 'Dmitriy'

from django import template

from store.catalog import models as store_models

register = template.Library()

@register.inclusion_tag('store/template_tags/print_price.html')
def print_price_link():
    price = store_models.Price.objects.get(pk=1)
    return {'price': price}


@register.simple_tag(name='price_url')
def price_url():
    price = store_models.Price.objects.get(pk=1)
    return price.file.url

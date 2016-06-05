__author__ = 'Dmitriy'

from django import template
from django.core import urlresolvers

from store.catalog import models as store_models

register = template.Library()

# Get url for modification
# specify_in_get - if true, modification={{ prod.modification.id }} will be added to url
@register.simple_tag(name='url_modification')
def url_modification(modification, specify_in_get = True):
    url = urlresolvers.reverse('item_page', args=[modification.item.id])
    if specify_in_get:
        url += '?modification=' + str(modification.id)
    return url


@register.filter
def index(List, i):
    return List[int(i)]


@register.inclusion_tag('store/template_tags/print_characteristic.html')
def print_characteristic(characteristic):
    return {'characteristic' : characteristic}

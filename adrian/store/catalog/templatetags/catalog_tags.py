__author__ = 'Dmitriy'

from store.catalog import models as store_models
from django import template
from django.core import urlresolvers

register = template.Library()

# Get url for modification
# specify_in_get - if true, modification={{ prod.modification.id }} will be added to url
@register.simple_tag(name='url_modification')
def url_modification(modification, specify_in_get = True):
    url = urlresolvers.reverse('item_page', args=[modification.item.id])
    if specify_in_get:
        url += '?modification=' + str(modification.id)
    return url
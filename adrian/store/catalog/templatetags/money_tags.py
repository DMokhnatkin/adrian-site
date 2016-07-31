import locale
from decimal import *

from django import template

from django.conf import settings

locale.setlocale(locale.LC_ALL, settings.LANGUAGE_CODE)
register = template.Library()


@register.filter(name='print_price')
def print_price(val):
    try:
        return locale.format("%d", Decimal(val), grouping=True)
    except:
        return '_'

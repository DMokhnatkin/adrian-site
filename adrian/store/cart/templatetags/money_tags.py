import locale
from decimal import *

from django import template

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

register = template.Library()

@register.filter(name='print_price')
def print_price(val):
    return locale.format("%d", Decimal(val), grouping=True)

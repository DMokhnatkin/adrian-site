from decimal import *

import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

from django import template
register = template.Library()

@register.filter(name='print_price')
def print_price(val):
    return locale.format("%d", Decimal(val), grouping=True)
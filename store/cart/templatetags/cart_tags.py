from decimal import *

from django import template
register = template.Library()

@register.inclusion_tag('store/cart/render_cart/full.html')
def render_full_cart(cart, render_toolbox=True):
    return {'products': cart,
            'render_toolbox': render_toolbox}

@register.inclusion_tag('store/cart/render_cart/preview.html')
def render_preview_cart(cart, render_toolbox=True):
    return {'products': cart,
            'render_toolbox': render_toolbox}
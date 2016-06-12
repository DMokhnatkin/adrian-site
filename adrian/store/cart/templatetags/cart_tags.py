from decimal import *

from django import template

from store.cart.utils import ProductsCart

register = template.Library()

@register.inclusion_tag('store/cart/render_cart/full.html')
def render_full_cart(cart, render_toolbox=True):
    return {'products': cart,
            'render_toolbox': render_toolbox}

@register.inclusion_tag('store/cart/render_cart/preview.html')
def render_preview_cart(cart, render_toolbox=True):
    return {'products': cart,
            'render_toolbox': render_toolbox}


@register.assignment_tag
def get_prod_cart(request):
    return ProductsCart.parse_from_request(request)

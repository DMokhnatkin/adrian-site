import threading

from django.shortcuts import render
from django.http.response import HttpResponseForbidden

from store.cart import apps as cart_settings
from . import utils
from store.cart import forms
from store.catalog import models as catalog_models

def cart_preview(request):
    if request.method == 'GET' and request.is_ajax():
        products = utils.ProductsCart.parse_from_request(request)
        return render(request, 'store/cart/render_cart/preview.html',
                      {'products': products,
                       'render_toolbox': True})
    return HttpResponseForbidden(request)


def cart_checkout(request):
    products = utils.ProductsCart.parse_from_request(request)
    if request.method == 'POST':
        form = forms.CheckoutForm(request.POST)
        if form.is_valid():
            user_data = {}
            for field in form.visible_fields():
                user_data[field.label] = form.cleaned_data[field.name]
            utils.notify_about_checkout(user_data, products)
            resp = render(request, 'store/cart/checkout/checkout_success.html', {'products': products})
            utils.ProductsCart.clear_in_response(resp)
            return resp
    else:
        form = forms.CheckoutForm()
    return render(request, 'store/cart/checkout/checkout.html',
                  {'products': products,
                   'form': form})

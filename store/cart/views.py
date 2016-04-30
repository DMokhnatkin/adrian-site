from django.shortcuts import render
from decimal import *
from django.conf import settings
from django.http import HttpResponseForbidden
from store.catalog import models as catalog_models
from store.cart import models as cart_models
from store.cart import forms


def cart_preview(request):
    if request.method == 'GET' and request.is_ajax():
        products = cart_models.ProductsList.parse_from_request(request)
        return render(request, 'store/cart/preview.html',
                      {'products': products})
    return HttpResponseForbidden(request)


def cart_checkout(request):
    products = cart_models.ProductsList.parse_from_request(request)
    if request.method == 'POST':
        form = forms.CheckoutForm(request.POST)
        if form.is_valid():
            return render(request, 'store/cart/checkout.html', {'products': products})
    else:
        form = forms.CheckoutForm()
    return render(request, 'store/cart/checkout.html',
                  {'products': products,
                   'form': form})

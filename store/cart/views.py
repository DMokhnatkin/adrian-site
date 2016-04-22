from django.shortcuts import render
from decimal import *
from django.conf import settings
import json
from django.http import HttpResponseForbidden
from store.catalog import models as catalog_models
from store.cart import models as cart_models


def cart_preview(request):
    if request.method == 'GET' and request.is_ajax():
        products = cart_models.ProductsList()
        try:
            prodList = json.loads(request.GET.get('products'))
            modifList = catalog_models.Modification.objects.filter(id__in = prodList.keys())
            for modif in modifList:
                prod = cart_models.Product(modif, prodList[str(modif.id)])
                products.add_product(prod)
        except Exception as e:
            if settings.DEBUG:
                raise e
        return render(request, 'store/cart/preview.html',
                      {'products': products})
    return HttpResponseForbidden(request)


def cart_checkout(request):
    return render(request, 'store/cart/checkout.html',
                  {})

__author__ = 'Dmitriy'
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
import json
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from store import models
from itemsFilter import forms as filter_forms
from itemsFilter import engine as filter_engine
from decimal import *
from django.conf import settings
from store.cart import cart


class ItemsInCategory(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id', None)
        category = models.Category.objects.get(id=category_id)

        if request.GET.get('clear', None) is not None:
            return redirect('items_in_category', category_id)

        return render(request, 'store/items_in_category.html',
            {"items": category.items(),
            "category": category,
            "filter": None})


def item_page(request, item_id):
    item = models.Item.objects.get(id=item_id)
    characteristic_table_data = {'characteristics': {}}
    has_not_none = bool
    for field_type in item.category.fieldtype_set.all():
        characteristic_table_data['characteristics'][field_type.title] = []
        has_not_none = False
        for modification in item.modification_set.all():
            if modification.get_characteristic(field_type).value is not None:
                has_not_none = True
                val = modification.get_characteristic(field_type).value
                if field_type.unit is not None:
                    val += ' ' + field_type.unit
                characteristic_table_data['characteristics'][field_type.title].append(val)
            else:
                characteristic_table_data['characteristics'][field_type.title].append('-')
        if not has_not_none:
            del characteristic_table_data['characteristics'][field_type.title]

    return render(request, 'store/item_page.html',
                  {'item': item,
                   'characteristic_table_data': characteristic_table_data,
                   'modifications': item.modifications})


def cart_preview(request):
    if request.method == 'GET' and request.is_ajax():
        items_in_cart = []
        common_price = {'val': Decimal(0), 'unit': None}
        try:
            prodList = json.loads(request.GET.get('products'))
            modifList = models.Modification.objects.filter(id__in = prodList.keys())
            for modif in modifList:
                prodInCart = cart.ProductInCart(modif, prodList[str(modif.id)])
                common_price['val'] += Decimal(prodInCart.comm_price)
                items_in_cart.append(prodInCart)
            # Get unit from first element
            if len(items_in_cart) > 0:
                common_price['unit'] = items_in_cart[0].unit
        except Exception as e:
            if settings.DEBUG:
                raise e
        return render(request, 'store/cart/preview.html',
                      {'items_in_cart': items_in_cart,
                       'common_price': common_price})
    return HttpResponseForbidden(request)


def cart_checkout(request):
    return render(request, 'store/cart/checkout.html',
                  {})


def home(request):
    return None
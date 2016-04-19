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
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8');


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
        items_in_cart = [];
        common_price = {'val': Decimal(0), 'formatted_val': None, 'unit': None};
        try:
            prodList = json.loads(request.GET.get('products'));
            modifList = models.Modification.objects.filter(id__in = prodList.keys());
            for modif in modifList:
                price = modif.get_characteristic_by_name('price');
                ct = prodList[str(modif.id)];
                val = Decimal(price.value) * Decimal(ct);
                common_price['val'] += Decimal(val);
                items_in_cart.append({'modification': modif,
                                      'count': ct,
                                      'comm_price': {'val': val,
                                                     'formatted_val': locale.format("%d", val, grouping=True),
                                                     'unit': price.unit()}});
            # Get unit from first element
            if len(items_in_cart) > 0:
                common_price['unit'] = items_in_cart[0]['comm_price']['unit'];
            common_price['formatted_val'] = locale.format("%d", common_price['val'], grouping=True);
        except Exception as e:
            if settings.DEBUG:
                return HttpResponse(e);
        return render(request, 'store/cart/preview.html',
                      {'items_in_cart': items_in_cart,
                       'common_price': common_price});
    return HttpResponseForbidden(request);

def home(request):
    return None
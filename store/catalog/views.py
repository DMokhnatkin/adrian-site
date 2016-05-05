__author__ = 'Dmitriy'
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from store.catalog import models

class ItemsInCategory(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id', None)
        category = models.Category.objects.get(id=category_id)

        if request.GET.get('clear', None) is not None:
            return redirect('items_in_category', category_id)

        return render(request, 'store/catalog/items_in_category.html',
            {"items": category.items(),
            "category": category,
            "filter": None})


def item_page(request, item_id):
    item = models.Item.objects.get(id=item_id)
    characteristic_table_data = {'characteristics': {}}
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

    return render(request, 'store/catalog/item_page.html',
                  {'item': item,
                   'characteristic_table_data': characteristic_table_data,
                   'modifications': item.modifications,
                   'selected_modifications': request.GET.getlist('modification')})


def home(request):
    return None
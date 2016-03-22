__author__ = 'Dmitriy'
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from store import models
from itemsFilter import forms as filter_forms
from itemsFilter import engine as filter_engine


class ItemsInCategory(View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id', None)
        category = models.Category.objects.get(id=category_id)

        if request.GET.get('clear', None) is not None:
            return redirect('items_in_category', category_id)

        conditions = filter_engine.FilterConditions()  # Conditions to filter items and modifications
        filter = filter_forms.FilterForm(request.GET, category=category)
        if request.GET.get('search', None) is not None:
            if filter.is_valid():
                for fieldtype in category.fieldtype_set.all():
                    # Try because we don't know if filtersetting and cleaned_data[fieldtype.name] are exists
                    try:
                        if fieldtype.filtersetting.active:
                            if filter.cleaned_data[fieldtype.name]:
                                if fieldtype.filtersetting.filter_type == 'range':
                                    val = filter.cleaned_data[fieldtype.name].split('|')
                                    conditions.add(filter_engine.FilterCond(gte=val[0] if val[0] != ''
                                                                                          and val[0] != 'None'
                                                                                          else None,
                                                                            lte=val[1] if val[1] != ''
                                                                                          and val[1] != 'None'
                                                                                          else None,
                                                                            field_name=fieldtype.name))
                    except:
                        pass
        filter_response = filter_engine.get_response(category_id, conditions)

        return render(request, 'store/items_in_category.html',
            {"items": filter_response.items,
            "category": category,
            "filter": filter})


def item_page(request, item_id):
    item = models.Item.objects.get(id=item_id)
    characteristic_tabel_data = {'modification_names': [],
                                 'characteristics': {}}
    for modification in item.modifications():
        characteristic_tabel_data['modification_names'].append(modification.name)
    has_not_none = bool
    for field_type in item.category.fieldtype_set.all():
        characteristic_tabel_data['characteristics'][field_type.title] = []
        has_not_none = False
        for modification in item.modification_set.all():
            if modification.get_characteristic(field_type).value is not None:
                has_not_none = True
                val = modification.get_characteristic(field_type).value
                if field_type.unit is not None:
                    val += ' ' + field_type.unit
                characteristic_tabel_data['characteristics'][field_type.title].append(val)
            else:
                characteristic_tabel_data['characteristics'][field_type.title].append('-')
        if not has_not_none:
            del characteristic_tabel_data['characteristics'][field_type.title]

    return render(request, 'store/item_page.html',
        {'item': item,
         'characteristic_table_data': characteristic_tabel_data,})


def home(request):
    return None
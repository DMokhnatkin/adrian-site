__author__ = 'Dmitriy'
from django.apps import apps
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from store.catalog import models


class ItemListView(ListView):
    """
    View with all items in category
    """
    model = models.Item
    template_name = 'store/catalog/items_in_category.html'

    def get_queryset(self):
        self.category = models.Category.objects.get(pk=self.kwargs['category_id'])
        return models.Item.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['items'] = self.object_list
        context['category'] = self.category
        context['render_cart'] = apps.is_installed('store.cart')
        return context


class ItemDetailView(DetailView):
    """
    View for single item
    """
    model = models.Item
    template_name = "store/catalog/item_page.html"

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        item = self.object
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

        context['item'] = item
        context['characteristic_table_data'] = characteristic_table_data
        context['modifications'] = item.modifications
        context['selected_modifications'] = self.request.GET.getlist('modification')
        context['render_cart'] = apps.is_installed('store.cart')
        return context

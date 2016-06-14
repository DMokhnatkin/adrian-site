__author__ = 'Dmitriy'

from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from store.catalog.views import ItemDetailView, ItemListView

urlpatterns = [
    url(r'^category/(?P<category_id>\d+)$', cache_page(60 * 30)(ItemListView.as_view()), name='items_in_category'),
    url(r'^item/(?P<pk>\d+)$', cache_page(60 * 30)(ItemDetailView.as_view()), name='item_page')
]

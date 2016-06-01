__author__ = 'Dmitriy'
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
from django.conf.urls.static import static

from store.catalog.views import ItemListView
from store.catalog.views import ItemDetailView
from django.conf import settings

urlpatterns = [
    url(r'^category/(?P<category_id>\d+)$', cache_page(60 * 30)(ItemListView.as_view()), name='items_in_category'),
    url(r'^item/(?P<pk>\d+)$', cache_page(60 * 30)(ItemDetailView.as_view()), name='item_page')
]
__author__ = 'Dmitriy'
from django.conf.urls import patterns, url
from store.catalog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^category/(?P<category_id>\d+)$', views.ItemsInCategory.as_view(), name='items_in_category'),
    url(r'^item/(?P<item_id>\d+)$', views.item_page, name='item_page')
]
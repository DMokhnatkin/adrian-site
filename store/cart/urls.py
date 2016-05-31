__author__ = 'Dmitriy'
from django.conf.urls import patterns, url
from django.views.decorators.cache import never_cache
from django.conf.urls.static import static

from store.cart import views

urlpatterns = [
    url(r'^cartPreview$', never_cache(views.cart_preview), name='cart_preview'),
    url(r'^checkout', never_cache(views.cart_checkout), name='cart_checkout')
]
__author__ = 'Dmitriy'
from django.conf.urls import patterns, url
from store.cart import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^cartPreview$', views.cart_preview, name='cart_preview'),
    url(r'^checkout', views.cart_checkout, name='cart_checkout')
]
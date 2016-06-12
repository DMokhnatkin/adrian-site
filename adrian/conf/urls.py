from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from contacts import views as contacts_views

urlpatterns = [
    url(
        r'^admin/',
        include(admin.site.urls)),
    url(
        r'^store/catalog/',
        include('store.catalog.urls')),
    url(
        r'^store/cart/',
        include('store.cart.urls')),
    url(
        r'^contacts$',
        contacts_views.contacts,
        name='contacts'),
    url(
        r'^services$',
        TemplateView.as_view(template_name='pages/services.html'),
        name='services'),
    url(
        r'^price$',
        TemplateView.as_view(template_name='pages/price.html'),
        name='price'),
    url(
        r'^$',
        TemplateView.as_view(template_name='pages/home.html'),
        name='home'),
]

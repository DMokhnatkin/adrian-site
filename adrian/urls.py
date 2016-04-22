"""adrian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

from contacts import views as contacts_views
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'adrian.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/catalog/', include('store.catalog.urls')),
    url(r'^store/cart/', include('store.cart.urls')),
    url(r'^contacts$', contacts_views.contacts, name='contacts'),
    url(r'^services$', TemplateView.as_view(template_name='pages/services.html'), name='services'),
    url(r'^price$', TemplateView.as_view(template_name='pages/price.html'), name='price'),
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
)

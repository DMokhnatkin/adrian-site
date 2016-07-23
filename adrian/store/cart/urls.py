__author__ = 'Dmitriy'
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from store.cart import views

urlpatterns = [
    url(r'^cartPreview$',
        never_cache(views.cart_preview),
        name='cart_preview'),
    url(r'^checkout$',
        never_cache(views.CheckoutView.as_view()),
        name='cart_checkout'),
    url(r'^checkout/success$',
        never_cache(views.CheckoutSuccessView.as_view()),
        name='checkout_success')
]

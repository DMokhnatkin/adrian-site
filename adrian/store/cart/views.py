import threading

from django.shortcuts import render
from django.http.response import HttpResponseForbidden

from store.cart import apps as cart_settings
from . import utils
from store.cart import forms
from store.catalog import models as catalog_models
from django.views.generic.base import ContextMixin
from django.views.generic import FormView, TemplateView, View


def cart_preview(request):
    if request.method == 'GET' and request.is_ajax():
        products = utils.Cart.parse_from_request(request)
        return render(request, 'store/cart/render_cart/preview.html',
                      {'products': products,
                       'render_toolbox': True})
    return HttpResponseForbidden(request)


class ProductsInCartMixin(View):
    """
    CBV builds ProductsCart from request
    """
    def get_products_cart(self):
        return utils.Cart.parse_from_request(self.request)

    def dispatch(self, request, *args, **kwargs):
        self.products_cart = self.get_products_cart()
        return super(ProductsInCartMixin, self).dispatch(request, *args, **kwargs)


class CheckoutView(ProductsInCartMixin, FormView):
    template_name = 'store/cart/checkout/checkout.html'
    success_url = 'checkout/success'
    form_class = forms.CheckoutForm

    def get_context_data(self, **kwargs):
        kwargs['products'] = self.products_cart
        return super(CheckoutView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user_data = {}
        for field in form.visible_fields():
            user_data[field.label] = form.cleaned_data[field.name]
        utils.notify_about_checkout(user_data, self.products_cart)
        return super(CheckoutView, self).form_valid(form)


class CheckoutSuccessView(ProductsInCartMixin, TemplateView):
    template_name = 'store/cart/checkout/checkout_success.html'

    def render_to_response(self, context, **response_kwargs):
        response = super(CheckoutSuccessView, self).render_to_response(context, **response_kwargs)
        utils.Cart.clear_in_response(response)
        return response

    def get_context_data(self, **kwargs):
        kwargs['products'] = self.products_cart
        return super(CheckoutSuccessView, self).get_context_data(**kwargs)


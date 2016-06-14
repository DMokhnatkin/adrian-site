import smtplib
import asyncio
from decimal import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.shortcuts import render
from django.template.loader import get_template

from django.conf import settings
from store.cart import apps as cart_settings
from . import utils
from store.cart import forms
from store.catalog import models as catalog_models


async def send_message():
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    msg = MIMEMultipart()
    msg['Subject'] = 'Заказ на сайте'
    msg['From'] = 'adrian-perm.ru'
    user_data = {}
    for field in form.visible_fields():
        user_data[field.label] = form.cleaned_data[field.name]
    msg.attach(
        MIMEText(
            get_template('store/cart/checkout/checkout_email.html').render(
                {'user_data': user_data,
                 'products': products}),
            'html'))

    server.sendmail(settings.EMAIL_HOST_USER, settings.CHECKOUT_EMAILS, msg.as_string())
    server.quit()

def cart_preview(request):
    if request.method == 'GET' and request.is_ajax():
        products = utils.ProductsCart.parse_from_request(request)
        return render(request, 'store/cart/render_cart/preview.html',
                      {'products': products,
                       'render_toolbox': True})
    return HttpResponseForbidden(request)


def cart_checkout(request):
    products = utils.ProductsCart.parse_from_request(request)
    if request.method == 'POST':
        form = forms.CheckoutForm(request.POST)
        if form.is_valid():

            resp = render(request, 'store/cart/checkout/checkout_success.html', {'products': products})
            utils.ProductsCart.clear_in_response(resp)
            return resp
    else:
        form = forms.CheckoutForm()
    return render(request, 'store/cart/checkout/checkout.html',
                  {'products': products,
                   'form': form})

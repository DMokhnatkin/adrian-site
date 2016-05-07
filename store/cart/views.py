from django.shortcuts import render
from decimal import *
from django.conf import settings
from django.http import HttpResponseForbidden
from store.catalog import models as catalog_models
from store.cart import models as cart_models
from store.cart import forms
from django.core.mail import send_mail
from store.cart import apps as cart_settings
from adrian import settings as adrian_settings
from django.template.loader import get_template

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def cart_preview(request):
    if request.method == 'GET' and request.is_ajax():
        products = cart_models.ProductsCart.parse_from_request(request)
        return render(request, 'store/cart/render_cart/preview.html',
                      {'products': products,
                       'render_toolbox': True})
    return HttpResponseForbidden(request)


def cart_checkout(request):
    products = cart_models.ProductsCart.parse_from_request(request)
    if request.method == 'POST':
        form = forms.CheckoutForm(request.POST)
        if form.is_valid():
            server = smtplib.SMTP(adrian_settings.EMAIL_HOST, adrian_settings.EMAIL_PORT)
            server.ehlo()
            server.starttls()
            server.login(adrian_settings.EMAIL_HOST_USER, adrian_settings.EMAIL_HOST_PASSWORD)
            msg = MIMEMultipart()
            msg['Subject'] = 'Заказ на сайте'
            msg['From'] = 'adrian-perm.ru'
            user_data = {}
            for field in form.visible_fields():
                user_data[field.label] = form.cleaned_data[field.name]
            msg.attach(
                MIMEText(
                    get_template('store/cart/checkout_email.html').render(
                        {'user_data': user_data,
                         'products': products}),
                    'html'))

            server.sendmail(adrian_settings.EMAIL_HOST_USER, cart_settings.StoreCartConfig.checkout_emails, msg.as_string())
            server.quit()
            resp = render(request, 'store/cart/checkout_success.html', {'products': products})
            cart_models.ProductsCart.clear_in_response(resp)
            return resp
    else:
        form = forms.CheckoutForm()
    return render(request, 'store/cart/checkout.html',
                  {'products': products,
                   'form': form})

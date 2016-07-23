import collections
import json
import smtplib
from decimal import *
from urllib import parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db import models
from django.conf import settings
from django.template import loader

from store.catalog.models import Modification
from store.catalog import utils as catalog_utils


def get_price(modification):
    """ (models.Modification) -> models.Characteristic
    Get price from database for modification.
    """
    field_type = catalog_utils.get_field_type(modification.item.category, 'price')
    return catalog_utils.get_value(modification, field_type)


# Represents item in cart
class CartItem:
    def __init__(self, modification, count):
        """
        :param modification: Some modification is a CartItem in cart
        :param count: Count of products
        :type modification: models.Modification
        :type count: int
        """
        self.modification = modification
        self.count = count
        try:
            price = get_price(modification)
            self.price = Decimal(price.value)
            self.unit = price.unit()
        except Exception:
            self.price = None
            self.unit = None
        self.__calc_total_price()

    def __calc_total_price(self):
        if self.price and self.count:
            self.total_price = Decimal(self.price) * Decimal(self.count)
        else:
            self.total_price = None


# Represents cart
class Cart:
    cookie_name = 'products_in_cart'

    @staticmethod
    def parse_from_request(request):
        cookies = request.COOKIES.get(Cart.cookie_name)
        if not cookies:
            return Cart()

        products_in_cookies = json.loads(
            parse.unquote(cookies),
            object_pairs_hook=collections.OrderedDict)
        if products_in_cookies:
            return Cart(source=products_in_cookies)
        else:
            return Cart()

    @staticmethod
    def clear_in_response(response):
        response.delete_cookie(Cart.cookie_name)

    def __init__(self, source=None, **kwargs):
        """
        :param source: Source to initialize
        :type source: OrderedDict, keys are modification id, values are count in cart
        """
        self.products = []
        self.total_price = Decimal(0)
        self.prod_count = 0
        if source:
            mdfs = Modification.objects.filter(pk__in=source.keys())
            for mod in mdfs:
                self.add_item(CartItem(mod, source[str(mod.id)]))

    def add_item(self, cart_item):
        """
        Add CartItem to cart and recalculate total_price
        :type cart_item: CartItem
        """
        self.products.append(cart_item)
        if cart_item.total_price:
            self.total_price += cart_item.total_price
        self.prod_count += cart_item.count

    def get_total_price_unit(self):
        if len(self.products) > 0:
            return self.products[0].unit
        else:
            return None

    def __iter__(self):
        return iter(self.products)

    def __len__(self):
        return self.prod_count

    def __nonzero__(self):
        return self.products.__nonzero__()


def notify_about_checkout(user_data, products):
    """
    Notify staff about checkout
    :param user_data: Info about user (from checkout form)
    :param products: ProductsCart
    """
    if type(products) is not Cart:
        raise TypeError('products must be instance of ProductsCart')
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    msg = MIMEMultipart()
    msg['Subject'] = 'Заказ на сайте'
    msg['From'] = 'adrian-perm.ru'
    msg.attach(
        MIMEText(
            loader.get_template('store/cart/checkout/checkout_email.html').render(
                {'user_data': user_data,
                 'products': products}),
            'html'))
    server.sendmail(settings.EMAIL_HOST_USER, settings.CHECKOUT_EMAILS, msg.as_string())
    server.quit()
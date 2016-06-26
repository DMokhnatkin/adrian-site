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


def get_price(modification):
    ''' (models.Modification) -> models.Characteristic
    Get price from database for modification.
    '''
    return modification.get_characteristic_by_name('price')


# Represents product in cart
class Product:
    def __init__(self, modification, count):
        '''
        :param modification: Some modification is a product in cart
        :param count: Count of products
        :type modification: models.Modification
        :type count: int
        '''
        self.modification = modification
        self.count = count
        price = get_price(modification)
        self.price = price.value
        self.unit = price.unit()
        self.__calc_total_price()

    def __calc_total_price(self):
        self.total_price = Decimal(self.price) * Decimal(self.count)


# Represents cart
class ProductsCart:
    cookie_name = 'products_in_cart'

    @staticmethod
    def parse_from_request(request):
        cookies = request.COOKIES.get(ProductsCart.cookie_name)
        if not cookies:
            return ProductsCart()

        products_in_cookies = json.loads(
            parse.unquote(cookies),
            object_pairs_hook=collections.OrderedDict)
        if products_in_cookies:
            return ProductsCart(source=products_in_cookies)
        else:
            return ProductsCart()

    @staticmethod
    def clear_in_response(response):
        response.delete_cookie(ProductsCart.cookie_name)

    def __init__(self, source=None, **kwargs):
        """
        :param source: Source to initialize
        :type source: OrderedDict, keys are modification id, values are count in cart
        """
        self.products = []
        self.total_price = Decimal(0)
        self.prod_count = 0
        if source is not None:
            mdfs = Modification.objects.filter(pk__in=source.keys())
            for mod in mdfs:
                self.add_product(Product(mod, source[str(mod.id)]))

    def add_product(self, product):
        """
        Add product to cart and recalculate total_price
        :type product: Product
        """
        self.products.append(product)
        self.total_price += product.total_price
        self.prod_count += product.count

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
    if type(products) is not ProductsCart:
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
import collections
import json
from decimal import *
from urllib import parse

from django.db import models

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
        products_in_cookies = json.loads(parse.unquote(cookies))
        if products_in_cookies:
            return ProductsCart(source=products_in_cookies.items())
        else:
            return ProductsCart()

    @staticmethod
    def clear_in_response(response):
        response.delete_cookie(ProductsCart.cookie_name)

    def __init__(self, source=None, **kwargs):
        '''
        :param source: Source to initialize
        :type source: Iterable, each cell of which is ('modification id', 'count in cart')
        '''
        self.products = []
        self.bad_products = [] # Products which are missing in database (maybe removed)
        self.total_price = Decimal(0)
        if source is not None:
            for mod_id, ct in source:
                mod = Modification.objects.get(id=mod_id)
                if mod is None:
                    self.bad_products.append({'id': mod_id, 'ct': ct})
                else:
                    self.add_product(Product(mod, ct))

    def add_product(self, product):
        '''
        Add product to cart and recalculate total_price
        :type product: Product
        '''
        self.products.append(product)
        self.total_price += product.total_price

    def get_total_price_unit(self):
        if len(self.products) > 0:
            return self.products[0].unit
        else:
            return None

    def __iter__(self):
        return iter(self.products)

    def __len__(self):
        return len(self.products)

    def __nonzero__(self):
        return self.products.__nonzero__()

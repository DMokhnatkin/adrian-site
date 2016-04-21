from store import models
from decimal import *


def get_price(modification):
    ''' (models.Modification) -> models.Characteristic
    Get price from database for modification.
    '''
    return modification.get_characteristic_by_name('price')


# Represents product in cart
class ProductInCart:
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
        self.__calc_comm_price()

    def __calc_comm_price(self):
        self.comm_price = Decimal(self.price) * Decimal(self.count)


# Represents cart
class Cart:
    products = []

    def __init__(self, products):
        products.extend(products)
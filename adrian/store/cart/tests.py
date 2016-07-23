from django.test import TestCase, RequestFactory

from .utils import CartItem
from .utils import Cart

from store.catalog.models import Modification


class CartItemTestCase(TestCase):
    fixtures = ['test_catalog.json']

    def test_price(self):
        z = CartItem(Modification.objects.get(pk=1), 3)
        self.assertEqual(z.price, 78000)

    def test_total_price(self):
        z = CartItem(Modification.objects.get(pk=2), 4)
        self.assertEqual(z.total_price, 44000)


class CartTestCase(TestCase):
    fixtures = ['test_catalog.json']

    def test_parse_from_request(self):
        request = RequestFactory().get('/#/')
        # Set {"1":2,"2":3,"3":1} to cookie
        request.COOKIES[Cart.cookie_name] = '{%221%22:2%2C%222%22:3%2C%223%22:1}'
        z = Cart.parse_from_request(request)
        self.assertEqual(z.prod_count, 6)
        self.assertEqual(z.total_price, 196000)


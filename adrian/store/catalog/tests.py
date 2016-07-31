from django.test import TestCase

from store.catalog.models import  Item


class CartItemTestCase(TestCase):
    fixtures = ['test_catalog.json']

    def test_price_range(self):
        self.assertEqual(
            Item.objects.get(pk=1).get_price_range()['low'],
            11000
        )
        self.assertEqual(
            Item.objects.get(pk=1).get_price_range()['hight'],
            78000
        )
        self.assertEqual(
            Item.objects.get(pk=1).get_price_range()['field_type'].name,
            'price'
        )



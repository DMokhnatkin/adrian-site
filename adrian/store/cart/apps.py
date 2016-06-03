from django.apps import AppConfig


class StoreCartConfig(AppConfig):
    name = 'store.cart'
    label = 'cart'
    checkout_emails = ['paparome@ya.ru']

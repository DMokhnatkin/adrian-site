from captcha.fields import ReCaptchaField
from django import forms
from django.utils.safestring import mark_safe
from phonenumber_field.formfields import PhoneNumberField

from store.cart import widgets


class CheckoutForm(forms.Form):
    address = forms.CharField(label='Адрес', max_length=100, widget=widgets.AddressWidget())
    phone = PhoneNumberField(label='Номер телефона')
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    captcha = ReCaptchaField(label='Вы человек?')
    error_css_class = 'error'

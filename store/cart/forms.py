from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(label='Адрес', max_length=100)
    phone = forms.CharField(label='Номер телефона', max_length=20)
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
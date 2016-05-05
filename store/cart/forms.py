from django import forms
from captcha.fields import ReCaptchaField

class CheckoutForm(forms.Form):
    address = forms.CharField(label='Адрес', max_length=100)
    phone = forms.CharField(label='Номер телефона', max_length=20)
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    captcha = ReCaptchaField()
    error_css_class = 'error'

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'Обязательное поле'
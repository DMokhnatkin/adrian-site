from django import forms
from captcha.fields import ReCaptchaField
from phonenumber_field.formfields import PhoneNumberField
from django.utils.safestring import mark_safe

class AddressWidget(forms.TextInput):
    class Media:
        js = ('js/store/cart/address_widget.js',
              'https://api-maps.yandex.ru/2.1/?lang=ru_RU',
              'https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js')
        css = {'all' : ('https://ajax.googleapis.com/ajax/libs/jqueryui/1.11.4/themes/smoothness/jquery-ui.css',)}
        
    def __init__(self, *args, **kwargs):
        super(AddressWidget, self).__init__(*args, **kwargs)
        if self.attrs and 'class' in self.attrs:
            self.attrs['class'] += ' address-field'
        else:
            self.attrs['class'] = 'address-field'

class CheckoutForm(forms.Form):
    address = forms.CharField(label='Адрес', max_length=100, widget=AddressWidget(attrs={'size':60}))
    phone = PhoneNumberField(label='Номер телефона')
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    captcha = ReCaptchaField()
    error_css_class = 'error'

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'Обязательное поле'
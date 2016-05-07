from django import forms

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
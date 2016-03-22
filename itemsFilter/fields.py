__author__ = 'Dmitriy'
from django import forms


# Range widget
class RangeWidget(forms.MultiWidget):
    def __init__(self, fields_type, min_val, max_val, def_low_val=None, def_up_val=None, attrs=None):
        self.min_val = min_val
        self.max_val = max_val
        self.def_low_val = def_low_val if def_low_val is not None else min_val
        self.def_up_val = def_up_val if def_up_val is not None else max_val
        widgets = []
        if fields_type is forms.IntegerField:
            widgets = [forms.NumberInput(attrs={'value': self.def_low_val,
                                                'class': "range lower"},),
                       forms.NumberInput(attrs={'value': self.def_up_val,
                                                'class': "range upper"})]
        super(RangeWidget, self).__init__(widgets, attrs)

    def format_output(self, rendered_widgets):
        return '<div class="widget range">' + rendered_widgets[0] + '-' + rendered_widgets[1] + '</div>'


# Range field for integer values in filter
class RangeIntegerField(forms.MultiValueField):
    def __init__(self, min_val=1, max_val=100000, def_low_val=None, def_up_val=None, *args, **kwargs):
        self.def_low_val = def_low_val if def_low_val is not None else min_val
        self.def_up_val = def_up_val if def_up_val is not None else max_val
        list_fields = [forms.IntegerField(min_value=min_val),
                       forms.IntegerField(max_value=max_val)]
        super(RangeIntegerField, self).__init__(list_fields,
                                                widget=RangeWidget(min_val=min_val,
                                                                   max_val=max_val,
                                                                   fields_type=forms.IntegerField),
                                                *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] == self.def_low_val:
                data_list[0] = None
            if data_list[1] == self.def_up_val:
                data_list[1] = None
            return str(data_list[0]) + '|' + str(data_list[1])

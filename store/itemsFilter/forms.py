__author__ = 'Dmitriy'
from django import forms

from store.itemsFilter import fields


# Form for filter
class FilterForm(forms.Form):
    # Depending on category, we will add fields to form
    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category')
        super(FilterForm, self).__init__(*args, **kwargs)
        if category is not None:
            for field in category.fieldtype_set.all():
                # filtersetting can not be exists
                try:
                    if field.filtersetting.active:
                        if field.filtersetting.filter_type == 'range':
                            if field.type() is int:
                                self.fields[field.name] = fields.RangeIntegerField(label=field.title, required=False)
                        if field.filtersetting.filter_type == 'MultipleChoice':
                            self.fields[field.name] = forms.MultipleChoiceField(label=field.title,
                                                                                choices=field.get_av_values())
                except:
                    pass
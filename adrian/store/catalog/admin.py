__author__ = 'Dmitriy'
from django import forms
from django.contrib import admin

from store.catalog import models


class CharacteristicForm(forms.ModelForm):
    class Meta:
        model = models.Characteristic
        exclude = ('field_type', 'modification')

    def __init__(self, *args, **kwargs):
        super(CharacteristicForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        # Lets change label for value fields
        if instance:
            self.fields['value'] = forms.CharField(label=instance.title(), required=False)


class CharacteristicInLine(admin.StackedInline):
    model = models.Characteristic
    extra = 0
    form = CharacteristicForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

class ModificationAdmin(admin.ModelAdmin):
    inlines = [CharacteristicInLine]
    list_display = ('name', 'item')
    list_filter = ['item']


class ModificationInLine(admin.StackedInline):
    model = models.Modification
    extra = 1


class ItemImageInLine(admin.StackedInline):
    model = models.ItemImage
    extra = 1


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ['category']
    inlines = [ItemImageInLine, ModificationInLine]


class FieldTypeInLine(admin.StackedInline):
    model = models.FieldType
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [FieldTypeInLine]


class PriceAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Modification, ModificationAdmin)
admin.site.register(models.Price, PriceAdmin)

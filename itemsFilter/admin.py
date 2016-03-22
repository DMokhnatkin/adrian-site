from django.contrib import admin
from itemsFilter import models as item_filter_models


class FilterSetting(admin.ModelAdmin):
    list_display = ('__str__', 'category',)


admin.site.register(item_filter_models.FilterSetting, FilterSetting)
from store import models as store_models
from django.db import connection
from django.db.models import Q


# Condition for one field
class FilterCond():
    field_name = None
    gte = None  # Greater or equal then
    lte = None  # Less or equal then
    equ = None  # Equal to

    def __init__(self, *args, **kwargs):
        self.gte = kwargs.get('gte', None)
        self.lte = kwargs.get('lte', None)
        self.equ = kwargs.get('equ', None)
        self.field_name = kwargs.get('field_name', None)


# Conditions to filter items
class FilterConditions():
    val = []

    def __init__(self):
        self.val = []

    # Add new filter condition
    def add(self, cond: FilterCond):
        self.val.append(cond)


# Filter will return FilterResponse object
# which contains items and modifications which
# where selected in filtration
class FilterResponse():
    items = []  # List of items
    modifications = []  # List of modifications

    def __init__(self, modifications=None):
        self.items = []
        self.modifications = []
        if modifications is not None:
            self.modifications = modifications
            # Get items from modifications
            for modification in self.modifications:
                if modification.item not in self.items:
                    self.items.append(modification.item)


# Get FilterResponse object which contains items and modifications under suitable conditions
def get_response(category_id: int, conditions: FilterConditions):
    # Select all modifications from category
    modifications = list(store_models.Modification.objects.filter(item__category=category_id))
    # Now let's filter this modifications
    for cond in conditions.val:
        query = 'select store_modification.id ' +\
                'from store_item, store_modification, store_characteristic, store_category, store_fieldtype ' +\
                    'where store_item.id = store_modification.item_id AND ' +\
                          'store_modification.id = store_characteristic.modification_id AND ' +\
                          'store_fieldtype.id = store_characteristic.field_type_id AND ' +\
                          'store_category.id = store_fieldtype.category_id AND ' +\
                          'store_item.category_id = store_category.id AND ' +\
                          'store_category.id = ''' + category_id
        field_cond = ''
        if cond.gte:
            field_cond += ' store_characteristic.value > ' + cond.gte
        if cond.lte:
            if cond.gte:
                field_cond += ' AND '
            field_cond += ' store_characteristic.value < ' + cond.lte
        if field_cond != '':
            query += ' AND IF(store_fieldtype.name = "' + cond.field_name + '", ' + field_cond + ', 0)'
        raw = store_models.Modification.objects.raw(query)
        new_modifications = []
        for modif in raw:
            if modif in modifications:
                new_modifications.append(modif)
        modifications = new_modifications
    return FilterResponse(modifications)


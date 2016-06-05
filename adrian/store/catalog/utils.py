from . import models


def get_field_types(category, sort_by_priority=False):
    """
    Get field types assosiated with some category
    :param category: Category
    :param sort_by_priority: Sort field types by priority
    """
    return models.FieldType.objects.filter(category=category).order_by('priority')


def get_modifications(item):
    """
    Get modifications for item
    :param item: item
    """
    return models.Modification.objects.filter(item=item)


def get_values(field_type, modifications):
    """
    Get field values
    :param modification: Modifications to get values
    :param field_types: Field type to get values
    """
    return models.Characteristic.objects.filter(
        field_type=field_type,
        modification__in=modifications)


class CharacteristicsTable:
    def __init__(self, item, exclude_empty=True):
        self.modifications = get_modifications(item)
        self.field_types = get_field_types(item.category, True)
        self.values = []
        for field_type in self.field_types:
            vals = get_values(field_type, self.modifications)
            not_empty = False
            for val in vals:
                if val.value:
                    not_empty = True
                    break
            if not_empty:
                self.values.append(get_values(field_type, self.modifications))
            else:
                self.values.append(None)

__author__ = 'Dmitriy'
from django.core import validators
from django.db import models
from django.db.models import signals, ExpressionWrapper, F
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории',
        unique='true')

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        unique='true')
    description = models.TextField(
        verbose_name='Описание')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория')

    def __str__(self):
        return self.name

    # Returns first related image
    def main_image(self):
        return self.itemimage_set.all()[0]

    def get_price_range(self):
        """
        Get price range (f.e. 100 rub. - 300 rub.)
        :return: {'low':Decimal, 'hight':Decimal, 'field_type':FieldType of price}
        """
        try:
            price_field_type = FieldType.objects.get(
                name='price',
                category=self.category
            )
            res = Characteristic.objects\
                .filter(
                    field_type=price_field_type,
                    modification__item=self
                )\
                .annotate(
                    price_decimal=ExpressionWrapper(
                        F('value'),
                        output_field=models.DecimalField()
                    )
                )\
                .aggregate(
                    low=models.Min('price_decimal'),
                    hight=models.Max('price_decimal')
                )
            res['field_type'] = price_field_type
            return res
        except models.ObjectDoesNotExist:
            return None


class ItemImage(models.Model):
    item = models.ForeignKey(Item)
    image = ThumbnailerImageField(
        upload_to='images/store',
        validators=[validators.RegexValidator(
            regex=r'^[\x00-\x7F]+$',
            message="Only ascii characters can be used")])


class Modification(models.Model):
    name = models.CharField(max_length=50)
    item = models.ForeignKey(Item)

    def __str__(self):
        return self.name

    def get_field_value(self, field_type):
        try:
            return Characteristic.objects.get(
                field_type=field_type,
                modification=self)
        except models.ObjectDoesNotExist:
            return None


# After creation Modification we must create characteristics and set null values
@receiver(signals.post_save, sender=Modification)
def constructor_modification(instance, **kwargs):
    if kwargs.get('created'):
        fields = instance.item.category.fieldtype_set.all()
        for field in fields:
            p = Characteristic(field_type=field, modification=instance, value=None)
            p.save()
    return None


# Type of field
class FieldType(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Системное имя',
        validators=[validators.RegexValidator(
            regex=r'^[a-zA-Z0-9_]+$',
            message="Only ascii characters can be used")])
    title = models.CharField(
        max_length=50,
        verbose_name='Имя')
    category = models.ForeignKey(Category)
    typeName = models.CharField('type', max_length=50, choices=(
        ('integer', 'Int'),
        ('string', 'String'),
        ('float', 'Float')),
        null=True)
    unit = models.CharField(
        max_length=30,
        verbose_name='Единицы измерения',
        null=True,
        blank=True)
    priority = models.IntegerField(
        default=0,
        verbose_name='Приоритет')

    def __str__(self):
        return self.category.name + ' - ' + self.title


# After FieldType creation we must create characteristic and set null value
# for all modifications which are in the same category as FieldType.
@receiver(signals.post_save, sender=FieldType)
def constructor_fieldtype(instance, **kwargs):
    if kwargs.get('created'):
        items = instance.category.item_set.all()
        for item in items:
            modifications = item.modification_set.all()
            for modification in modifications:
                new_characteristic = Characteristic(field_type=instance, modification=modification)
                new_characteristic.save()
    return None


# Characteristic is used to connect modification, field_type and value
class Characteristic(models.Model):
    modification = models.ForeignKey(Modification)
    field_type = models.ForeignKey(FieldType)
    value = models.CharField(
        max_length=5000,
        null=True,
        verbose_name='Значение')

    def __str__(self):
        return self.field_type.name

    def title(self):
        return self.field_type.title

    def unit(self):
        return self.field_type.unit


# Price for catalog
class Price(models.Model):
    file = models.FileField(
        upload_to='files')
    label = models.CharField(
        max_length=50,
        default="")

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slideshows', '0002_auto_20150319_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='description',
            field=models.CharField(blank=True, max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='slide',
            name='label',
            field=models.CharField(blank=True, max_length=50),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20160615_0113'),
    ]

    operations = [
        migrations.AddField(
            model_name='modification',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

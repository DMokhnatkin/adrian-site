# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_price_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristic',
            name='value',
            field=models.CharField(max_length=5000, blank=True, null=True),
        ),
    ]

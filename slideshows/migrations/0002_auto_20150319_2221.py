# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slideshows', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slideshow',
            name='name',
            field=models.CharField(max_length=50, unique=True),
            preserve_default=True,
        ),
    ]

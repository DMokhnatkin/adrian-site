# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-04 18:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtype',
            name='typeName',
            field=models.CharField(choices=[('integer', 'Int'), ('string', 'String'), ('float', 'Float')], default=True, max_length=50, verbose_name='type'),
        ),
    ]

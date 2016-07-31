# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 18:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_remove_modification_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecimalFieldStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_val', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IntegerFieldStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_val', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='fieldtype',
            name='valueType',
            field=models.SmallIntegerField(choices=[(0, 'Decimal'), (1, 'Integer')], default=-1, verbose_name='Value type'),
        ),
        migrations.AddField(
            model_name='integerfieldstorage',
            name='field_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.FieldType'),
        ),
        migrations.AddField(
            model_name='integerfieldstorage',
            name='modification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Modification'),
        ),
        migrations.AddField(
            model_name='decimalfieldstorage',
            name='field_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.FieldType'),
        ),
        migrations.AddField(
            model_name='decimalfieldstorage',
            name='modification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.Modification'),
        ),
    ]

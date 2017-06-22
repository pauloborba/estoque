# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20170527_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='enough',
        ),
        migrations.AddField(
            model_name='item',
            name='min_qty',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='item',
            name='qty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('category_name', 'category_store')]),
        ),
    ]

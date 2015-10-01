# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import dealmonkapp.models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('dealmonkapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriesFactTable',
            fields=[
                ('category_id', models.AutoField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(default=None, max_length=45, blank=True)),
                ('category_create_date', models.DateTimeField(null=True, blank=True)),
                ('category_create_by', models.CharField(default=None, max_length=45, blank=True)),
                ('category_update_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('category_update_by', models.CharField(default=None, max_length=45, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItemTable',
            fields=[
                ('menu_item_id', models.AutoField(serialize=False, primary_key=True)),
                ('category_name', models.CharField(default=None, max_length=45, verbose_name=dealmonkapp.models.CategoriesFactTable, blank=True)),
                ('menu_item_name', models.CharField(default=None, max_length=45, blank=True)),
                ('menu_item_price', models.IntegerField(default=None, blank=True)),
                ('menu_item_type', models.CharField(default=None, max_length=45, choices=[(b'VEG', b'VEG'), (b'GLUTEN FREE', b'GLUTEN FREE'), (b'NON-VEG', b'NON-VEG')])),
                ('menu_item_create_date', models.DateTimeField(null=True, blank=True)),
                ('menu_item_create_by', models.CharField(default=None, max_length=45, blank=True)),
                ('menu_item_update_date', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('menu_item_update_by', models.CharField(default=None, max_length=45, blank=True)),
                ('menu_item_status', models.CharField(default=1, max_length=1)),
                ('category_id', models.ForeignKey(default=None, blank=True, to='dealmonkapp.CategoriesFactTable', null=True)),
                ('restaurant_id', models.ForeignKey(default=None, blank=True, to='dealmonkapp.Restaurant', null=True)),
            ],
        ),
    ]

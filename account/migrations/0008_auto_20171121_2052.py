# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-21 19:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20171121_2046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wiadomosc',
            old_name='data_wyslawana',
            new_name='data_wyslania',
        ),
    ]

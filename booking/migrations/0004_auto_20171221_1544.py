# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-21 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20171215_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magazines',
            name='staff',
            field=models.ManyToManyField(blank=True, to='booking.Staff'),
        ),
    ]

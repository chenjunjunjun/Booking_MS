# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-10 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart_name', models.CharField(max_length=20)),
                ('depart_num', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Magazines',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mag_name', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('comment', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_name', models.CharField(max_length=20)),
                ('staff_number', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=20)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Department')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='magazines',
            name='staff',
            field=models.ManyToManyField(to='booking.Staff'),
        ),
    ]

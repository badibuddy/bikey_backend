# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-10-20 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.IntegerField(choices=[(0, 'Parts'), (1, 'Mechanics'), (2, 'Gear'), (3, 'Events'), (4, 'Regulations'), (5, 'Stories')], default=5),
        ),
    ]

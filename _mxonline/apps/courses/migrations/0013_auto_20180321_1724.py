# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-21 17:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_courseorg_org_tag'),
        ('courses', '0012_auto_20180321_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='id_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
    ]

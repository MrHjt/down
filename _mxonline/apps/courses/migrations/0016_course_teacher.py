# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-21 19:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_courseorg_org_tag'),
        ('courses', '0015_auto_20180321_1915'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='course',
        #     name='teacher',
        #     field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='讲师'),
        # ),
    ]

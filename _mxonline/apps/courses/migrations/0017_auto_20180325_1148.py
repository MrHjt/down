# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-25 11:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_course_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCourse',
            fields=[
            ],
            options={
                'verbose_name': '轮播课程',
                'verbose_name_plural': '轮播课程',
                'proxy': True,
                'indexes': [],
            },
            bases=('courses.course',),
        ),
        migrations.AddField(
            model_name='course',
            name='add_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='添加时间'),
        ),
    ]

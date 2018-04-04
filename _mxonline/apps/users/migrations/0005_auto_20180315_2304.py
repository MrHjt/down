# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-15 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180315_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '密码'), ('update_email', '修改邮箱')], max_length=30, verbose_name='发送类型'),
        ),
    ]
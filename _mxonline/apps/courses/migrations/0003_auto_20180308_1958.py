# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-08 19:58
from __future__ import unicode_literals

import DjangoUeditor.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_teacher_image'),
        ('courses', '0002_course_course_org'),
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
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': '章节', 'verbose_name_plural': '章节'},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'verbose_name': '视频', 'verbose_name_plural': '视频'},
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='后端开发', max_length=20, verbose_name='课程类别'),
        ),
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=10, verbose_name='课程标签'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='讲师'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(default='', max_length=300, verbose_name='老师告诉你'),
        ),
        migrations.AddField(
            model_name='course',
            name='youneed_know',
            field=models.CharField(default='', max_length=300, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
        migrations.AddField(
            model_name='video',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='访问地址'),
        ),
        migrations.AlterField(
            model_name='course',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('cj', '初级'), ('zj', '中级'), ('gj', '高级')], max_length=2, verbose_name='难度'),
        ),
        migrations.AlterField(
            model_name='course',
            name='desc',
            field=models.CharField(max_length=300, verbose_name='课程描述'),
        ),
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='课程详情'),
        ),
        migrations.AlterField(
            model_name='course',
            name='fav_nums',
            field=models.IntegerField(default=0, verbose_name='收藏人数'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='course',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=50, verbose_name='课程名'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='courseresource',
            name='name',
            field=models.CharField(max_length=100, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(max_length=100, verbose_name='章节名'),
        ),
        migrations.AlterField(
            model_name='video',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='video',
            name='name',
            field=models.CharField(max_length=100, verbose_name='视频名'),
        ),
    ]
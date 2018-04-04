#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from DjangoUeditor.models import UEditorField

from django.db import models


# Create your models here.

class CityDict(models.Model):
    name=models.CharField(max_length=20,verbose_name=u"城市名称");
    desc=models.TextField(verbose_name=u"描述",max_length=200);
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间");

    class Meta:
        verbose_name=u"城市";
        verbose_name_plural=verbose_name;

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name=models.CharField(max_length=50,verbose_name=u"机构名称");
    # desc=models.TextField(verbose_name=u"机构描述");
    desc = UEditorField(verbose_name=u'机构详情	',width=600, height=300, toolbars="full", imagePath="orgs/ueditor/",
                        filePath="orgs/ueditor/",default='');
    catgory=models.CharField(default='pxjg',verbose_name=u'机构类别',max_length=20,choices=(("pxjg",'培训机构'),('gx','高校'),('gr','个人')))
    click_nums=models.IntegerField(default=0,verbose_name=u"点击数目");
    fav_nums=models.IntegerField(default=0,verbose_name=u"收藏数");
    org_tag=models.CharField(default=u"全国知名",verbose_name='标签',max_length=10)
    image=models.ImageField(upload_to="org/%Y/%m",verbose_name=u"封面图",max_length=100);
    address=models.CharField(max_length=150,default="",verbose_name=u"机构地址");
    city=models.ForeignKey(CityDict,verbose_name=u"所在城市");
    students=models.IntegerField(default=0,verbose_name=u"学习人数");
    course_nums=models.IntegerField(default=0,verbose_name=u"课程数目");
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间");

    class Meta:
        verbose_name=u"课程机构";
        verbose_name_plural=verbose_name;

    def __str__(self):
        return self.name


    def get_teacher_nums(self):
        #
        return self.teacher_set.all().count();


class Teacher(models.Model):
    org=models.ForeignKey(CourseOrg,verbose_name=u"所属机构");
    name=models.CharField(max_length=50,verbose_name=u"教师名称");
    image=models.ImageField(upload_to="tearch/%Y/%m",verbose_name=u"教师照片",max_length=100,default='',null=True,blank=True);
    work_years=models.IntegerField(default=0,verbose_name=u"工作年限")
    work_company=models.CharField(max_length=50,verbose_name=u"就职公司")
    work_position=models.CharField(max_length=50,verbose_name=u"公司职位")
    points=models.CharField(max_length=50,verbose_name=u"教学特点");
    click_nums=models.IntegerField(default=0,verbose_name=u"点击数目");
    fav_nums=models.IntegerField(default=0,verbose_name=u"收藏数");
    age = models.IntegerField(default=18, verbose_name=u"年龄")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间");


    class Meta:
        verbose_name=u"教师";
        verbose_name_plural=verbose_name;

    def __str__(self):
        return self.name


    def get_courses(self):
        return self.course_set.all().count();

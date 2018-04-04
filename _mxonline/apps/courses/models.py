#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from DjangoUeditor.models import UEditorField
from django.db import models
from  organization.models import CourseOrg,Teacher

# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    # desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    desc = UEditorField(verbose_name=u'课程详情	',width=600, height=300, imagePath="courses/ueditor/",
                        filePath="courses/ueditor/",blank=True,default='')
    detail = models.CharField(max_length=300, verbose_name=u"课程描述")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播",max_length=20)
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    degree = models.CharField(verbose_name=u"难度", choices=(("cj","初级"), ("zj","中级"), ("gj","高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default=u"后端开发", max_length=20, verbose_name=u"课程类别")
    tag = models.CharField(default="", verbose_name=u"课程标签", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name=u"课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name=u"老师告诉你");

    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间",null=True,blank=True);


    class Meta:
        verbose_name=u"课程";
        verbose_name_plural=verbose_name;

    def __str__(self):
        return self.name;

    def get_zj_nums(self):
        return self.lesson_set.all().count();

    get_zj_nums.short_description='章节数'


    def learn_student(self):
        return self.usercourse_set.all()[:3];

    def get_course_lesson(self):
        #获取章节数目
        return self.lesson_set.all()


    def get_course_resource(self):
        return self.courseresource_set.all()


class BannerCourse(Course):
    class Meta:
        verbose_name=u'轮播课程';
        verbose_name_plural=verbose_name;
        proxy=True



class Lesson(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程");
    name=models.CharField(max_length=100,verbose_name=u"章节名称")
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间",null=True,blank=True);

    class Meta:
        verbose_name=u"课程章节";
        verbose_name_plural=verbose_name;


    def __str__(self):
        return self.name;

    def get_lesson_video(self):
        #获取章节视频
        return self.video_set.all();

class Video(models.Model):
    lesson=models.ForeignKey(Lesson,verbose_name=u"章节");
    name=models.CharField(max_length=100,verbose_name=u"视频名称")
    url= models.CharField(default='',max_length=300,verbose_name=u"视频链接");
    learn_times=models.IntegerField(default=0,verbose_name=u"分钟数");
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间",null=True,blank=True);

    class Meta:
        verbose_name=u"课程视频";
        verbose_name_plural=verbose_name;


    def __str__(self):
        return self.name

class CourseResource(models.Model):
    course=models.ForeignKey(Course,verbose_name=u"课程");
    name=models.CharField(max_length=100,verbose_name=u"资源名称")
    download=models.FileField(upload_to="course/resource/%Y/%m",verbose_name=u"资源文件",max_length=100);
    add_time=models.DateTimeField(default=datetime.now,verbose_name=u"添加时间",null=True,blank=True);


    class Meta:
        verbose_name=u"课程资源";
        verbose_name_plural=verbose_name;


    def __str__(self):
        return self.name


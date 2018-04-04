#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xadmin

from .models import Course,Lesson,Video,CourseResource,BannerCourse
# Register your models here.

class LessonInline(object):
    model=Lesson;
    extra=0


class CourseResourceInline(object):
    model=CourseResource;
    extra=0;

class Courseadmin(object):
    list_display = ['name','desc','detail','teacher','get_zj_nums','is_banner','learn_times','students'];
    #排序
    ordering=['-learn_times'];
    #只读
    readonly_fields=['learn_times'];
    #隐藏
    exclude=['fav_nums'];
    inlines=[LessonInline,CourseResourceInline];
    style_fields = {"detail":"ueditor"}
    import_excel = True

    def queryset(self):
        qs=super(Courseadmin,self).queryset();
        qs=qs.filter(is_banner=False);
        return qs

    def save_models(self):
        obj=self.new_obj;
        obj.save();
        if obj is not None:
            course_org=obj.course_org;
            course_org.course_nums=Course.objects.filter(course_org=course_org).count();
            course_org.save();

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(Courseadmin, self).post(request, args, kwargs)

class BannerCourseAdmin(object):
    list_display = ['name', 'desc','detail','detail','teacher','get_zj_nums','is_banner','learn_times','students'];
    #排序
    ordering=['-learn_times'];
    #只读
    readonly_fields=['learn_times'];
    #隐藏
    exclude=['fav_nums'];
    inlines=[LessonInline,CourseResourceInline];
    list_editable=['desc','detail']


    def queryset(self):
        qs=super(BannerCourseAdmin,self).queryset();
        qs=qs.filter(is_banner=True);
        return qs

class Lessonadmin(object):
    pass


class Videoadmin(object):
    pass


class CourseResourceadmin(object):
    pass


xadmin.site.register(CourseResource,CourseResourceadmin);
xadmin.site.register(BannerCourse,BannerCourseAdmin);
xadmin.site.register(Course,Courseadmin);
xadmin.site.register(Video,Videoadmin);
xadmin.site.register(Lesson,Lessonadmin);

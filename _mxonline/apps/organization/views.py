#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from django.db.models import Q

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from courses.models import Course
from users.models import UserProfile
from operation.models import UserFavorite
from .models import Teacher


class OrgView(View):
    # 课程机构列表功能
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all();
        current_nav='org';
        # 城市
        all_city = CityDict.objects.all()
        hot_course = all_orgs.order_by("-click_nums")[:3];
        #搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))
        # 学习人数排序
        sort = request.GET.get("sort", "");
        if sort:

            if sort == "students":
                all_orgs = all_orgs.order_by("-students");
            # 课程数目
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums");
        # 城市筛选
        city_num = request.GET.get("city", "");
        if city_num:
            all_orgs = all_orgs.filter(city_id=int(city_num));

        # 类别筛选

        category = request.GET.get("ct", "");
        if category:
            all_orgs = all_orgs.filter(catgory=category)
        org_count = all_orgs.count();
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs,2,request=request)

        orgs = p.page(page)
        # paginator = Paginator(all_orgs, 5)
        # page = request.GET.get('page')
        # try:
        #     contacts = paginator.page(page)
        # except PageNotAnInteger:
        #     contacts = paginator.page(1)
        # except EmptyPage:
        #     contacts = paginator.page(paginator.num_pages)

        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_count": org_count,
            "all_city": all_city,
            "hot_course": hot_course,
            "sort": sort,
            "city_num": city_num,
            'category': category,
            'current_nav':current_nav
        }
                      )


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST);
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True);
            return HttpResponse('{"status":"success"}', content_type='application/json');
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json');


class OrgHomeView(View):
    # 机构首页
    def get(self, request, org_id):
        current_page = 'home';
        course_org = CourseOrg.objects.get(id=int(org_id));
        course_org.click_nums +=1;
        course_org.save();
        has_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True;
        all_coures = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1];
        return render(request, 'org-detail-homepage.html', {
            'all_coures': all_coures,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        }
                      )


class OrgCourseView(View):
    # 机构课程
    def get(self, request, org_id):
        current_page = 'course';
        course_org = CourseOrg.objects.get(id=int(org_id));
        has_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True;
        all_coures = course_org.course_set.all()

        return render(request, 'org-detail-course.html', {
            'all_coures': all_coures,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        }
                      )


class OrgDescView(View):
    # 机构描述
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id));
        has_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True;

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        }
                      )


class OrgTeacherView(View):
    # 机构首页
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id));
        has_fav=False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav=True;
        all_coures = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1];
        return render(request, 'org-detail-teachers.html', {
            'all_coures': all_coures,
            'all_teacher': all_teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav':has_fav
        }
                      )


class AddFavView(View):
    """
    用户收藏，用户取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在， 则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teacher=Teacher.objects.all();
        current_nav='teacher';
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_teacher = all_teacher.filter(Q(name__icontains=search_keywords)|
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))
        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        sort=request.GET.get('sort','');
        if sort:
            if sort == 'hot':
                all_teacher=all_teacher.order_by('-click_nums')
         #对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, 5, request=request)

        teachers = p.page(page)
        return render(request,'teachers-list.html',{
            'all_teacher':teachers,
            'sorted_teachers':sorted_teachers,
            'sort':sort,
            'current_nav':current_nav
        })


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        teacher=Teacher.objects.get(id=int(teacher_id));
        teacher.click_nums += 1
        teacher.save()
        courses=Course.objects.filter(teacher=teacher);
        has_teacher_faved = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=int(teacher.id)):
                has_teacher_faved = True

        has_org_faved = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=int(teacher.org.id)):
                has_org_faved = True

        return render(request,'teacher-detail.html',{
            'sorted_teachers':sorted_teachers,
            'teacher':teacher,
            'courses':courses,
            'has_teacher_faved':has_teacher_faved,
            'has_org_faved':has_org_faved
        })




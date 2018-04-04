#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
import json
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse


from .models import UserProfile,EmailVerifyRecord,Banner
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm
from utils.email_send import send_register_email
# Create your views here.
from utils.mixin_utils import LoginRequiredMixin
from .forms import UserInfoForm,UploadImageForm
from operation.models import UserCourse,UserFavorite,UserMessage
from courses.models import Course
from organization.models import CourseOrg,Teacher




class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username)|Q(email=username));
            if user.check_password(password):
                return user;
        except Exception as e:
            return None;


# class CustomBackkend()
class LoginView(View):
    def get(self,request):
        return render(request,"login.html",{});
    def post(self,request):
        login_form=LoginForm(request.POST);
        if login_form.is_valid():
            user_name=request.POST.get("username","");
            pass_word=request.POST.get("password","");
            user=authenticate(username=user_name,password=pass_word);
            if user is not None:
                if user.is_active:
                  login(request,user);
                  return HttpResponseRedirect(reverse("index"));
                else:
                    return render(request,"login.html",{"msg":"用户未激活！"})
            else:
                return render(request,"login.html",{"msg":"用户名或者密码错误！"});
        else:
            return render(request,"login.html",{"login_form":login_form});



class LoginOutView(View):
    def get(self,request):
        logout(request);
        return HttpResponseRedirect(reverse("index"));

class ActiveUserView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code);
        if all_records:
            for record in all_records:
                email=record.email;
                user=UserProfile.objects.get(email=email);
                user.is_active=True;
                user.save();
        else:
            return render(request,"active_fail.html",{});
        return render(request,"login.html",{});



class RegisterView(View):
    def get(self,request):
        register_form=RegisterForm(request.POST);
        return render(request,'register.html',{'register_form':register_form});
    def post(self,request):
        register_form=RegisterForm(request.POST);
        if register_form.is_valid():
            user_name=request.POST.get("email","");
            if UserProfile.objects.filter(email=user_name):
                 return render(request,"register.html",{'register_form':register_form,"msg":u"该邮箱已存在！"})
            pass_word=request.POST.get("password","");
            user_profile=UserProfile();
            user_profile.username=user_name;
            user_profile.email=user_name;
            user_profile.password=make_password(pass_word);
            user_profile.is_active=False;
            user_profile.save();

            user_message=UserMessage();
            user_message.user=user_profile.id;
            user_message.message='欢迎注册慕学网';
            user_message.has_read='False';
            user_message.save()

            send_register_email(user_name,"register");

            return render(request,"login.html",{});
        else:
            return render(request,"register.html",{'register_form':register_form});


def user_login(request):
    if request.method=='POST':
        user_name=request.POST.get("username","");
        pass_word=request.POST.get("password","");
        user=authenticate(username=user_name,password=pass_word);
        if user is not None:
            login(request,user);
            return render(request,"index.html")
        else:
            return render(request,"login.html",{"msg":"用户名或者密码错误！"});
    elif request.method=='GET':
        return render(request,"login.html",{});


class ForgetPwdView(View):
    def get(self,request):
        forget_form=ForgetForm();
        return render(request,"forgetpwd.html",{"forget_form":forget_form});
    def post(self,request):
        forget_form=ForgetForm(request.POST);
        if forget_form.is_valid():
            email=request.POST.get("email","");
            send_register_email(email,"forget");
            return render(request,"send_success.html");
        else:
            return render(request,"forgetpwd.html",{"forget_form":forget_form})


class ResetView(View):
    def get(self,request,active_code):
        all_records=EmailVerifyRecord.objects.filter(code=active_code);
        if all_records:
            for record in all_records:
                email=record.email;
                return render(request,"password_reset.html",{"email":email});
        else:
            return render(request,"active_fail.html",{});
        return render(request,"login.html",{});


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form})


class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html',{})

    def post(self,request):
        user_info_from=UserInfoForm(request.POST,instance=request.user);
        if user_info_from:
            user_info_from.save();
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_from.errors), content_type='application/json')


class UploadImageView(View):
    def post(self,request):
        upload_image=UploadImageForm(request.POST,request.FILES,instance=request.user);
        if upload_image.is_valid():
            upload_image.save();
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}',content_type='application/json');



class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")

            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',content_type='application/json')
            user = request.user;
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),content_type='application/json')



class SendEmailCodeView(LoginRequiredMixin,View):
    #发送邮箱验证码
    def get(self,request):
        email=request.GET.get("email",'');
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经被注册!"}',content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse('{"email":"success!"}',content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email=request.POST.get("email","");
        code=request.POST.get("code","");
        existed=EmailVerifyRecord.objects.filter(email=email,code=code,send_type="update_email");
        if existed:
            user=request.user;
            user.email=email;
            user.save();
            return HttpResponse('{"email":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误!"}',content_type='application/json')


class MyCourseView(View):
    def get(self,request):
        courses=UserCourse.objects.filter(user=request.user);

        return render(request,'usercenter-mycourse.html',{
            "mycourses":courses
        })


class MyFavCourseView(View):
    #我的收藏课程
    def get(self,request):
        myfav_couses=UserFavorite.objects.filter(user=request.user,fav_type=1);

        course_list=[];
        for course in myfav_couses:
            course_id=course.fav_id;
            course=Course.objects.get(id=course_id);
            course_list.append(course);


        return render(request,'usercenter-fav-course.html',{
        'course_list':course_list
        })




class MyFavOrgView(View):
    #我的收藏机构
    def get(self,request):
        myfav_org=UserFavorite.objects.filter(user=request.user,fav_type=2);

        org_list=[];
        for org in myfav_org:
            org_id=org.fav_id;
            org=CourseOrg.objects.get(id=org_id);
            org_list.append(org);


        return render(request,'usercenter-fav-org.html',{
        'org_list':org_list
        })


class MyFavTeacherView(View):
    #我的收藏教师
    def get(self,request):
        myfav_teacher=UserFavorite.objects.filter(user=request.user,fav_type=3);

        teacher_list=[];
        for teacher in myfav_teacher:
            teacher_id=teacher.fav_id;
            teacher=Teacher.objects.get(id=teacher_id);
            teacher_list.append(teacher);


        return render(request,'usercenter-fav-teacher.html',{
        'teacher_list':teacher_list
        })


class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        messages=UserMessage.objects.filter(user=request.user.id);
        unread_message=UserMessage.objects.filter(user=request.user.id,has_read=False);
        for unread in unread_message:
            unread.has_read=True;
            unread.save();

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, 1, request=request)

        message = p.page(page)
        return render(request,'usercenter-message.html',{
            'messages':message

        })


class IndexView(View):
    def get(self,request):
        all_banner=Banner.objects.all().order_by('index');

        courses_banner=Course.objects.filter(is_banner=True)[:3];
        courses=Course.objects.filter(is_banner=False)[:6];

        orgs=CourseOrg.objects.all()[:15];

        return render(request,'index.html',{
            'all_banner':all_banner,
            'courses_banner':courses_banner,
            'courses':courses,
            'orgs':orgs

        })


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
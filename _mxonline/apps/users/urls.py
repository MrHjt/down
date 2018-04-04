#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url,include


from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,\
    UpdateEmailView,MyCourseView,MyFavCourseView,MyFavOrgView,MyFavTeacherView,MyMessageView




urlpatterns = [
    url(r'^info/$',UserInfoView.as_view(),name='user_info'),
    #修改头像
    url(r'^upload/image',UploadImageView.as_view(),name='upload_image'),
    url(r'^update/pwd',UpdatePwdView.as_view(),name='update_pwd'),
    #发送邮箱验证码
    url(r'^sendemail_code',SendEmailCodeView.as_view(),name='sendemail_code'),
    #修改邮箱
    url(r'^update_email',UpdateEmailView.as_view(),name='update_email'),
    #我的课程
    url(r'^mycourse',MyCourseView.as_view(),name='mycourse'),
     #我的课程收藏
    url(r'^myfav_course',MyFavCourseView.as_view(),name='myfav_course'),
      #我的机构收藏
    url(r'^myfav_org',MyFavOrgView.as_view(),name='myfav_org'),
    #我的教师收藏
    url(r'^myfav_teacher',MyFavTeacherView.as_view(),name='myfav_teacher'),
     #我的信息
    url(r'^my/messages',MyMessageView.as_view(),name='mymessages')




]

from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Course,Video,Lesson,CourseResource,Video
from operation.models import CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CoursesListView(View):
    def get(self,request):
        all_courses=Course.objects.all().order_by("-add_time");
        order_course=all_courses.order_by("-click_nums")[:3]
        current_nav='course';
        keywords=request.GET.get('keywords','');
        if keywords:
            all_courses=all_courses.filter(Q(name__contains=keywords)|Q(desc__contains=keywords)|Q(desc__contains=keywords))
        sort= request.GET.get("sort",'');
        if sort:
            if sort=='hot':
                all_courses=all_courses.order_by('-click_nums');
            elif sort=='students':
                all_courses=all_courses.order_by('-students')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses,2,request=request)
        cours = p.page(page)

        return render(request,'course-list.html',{
            'all_courses':cours,
            'order_course':order_course,
            'sort':sort,
            'current_nav':current_nav
          }
         )


class CourseDetailView(View):
    def get(self,request,course_id):
        course_detail=Course.objects.get(id=int(course_id));
        #增加课程点击数
        course_detail.click_nums +=1;
        course_detail.save();


        tag=course_detail.tag;
        if tag:
            relate_course=Course.objects.filter(tag=tag)[:2];
        else:
            relate_course=[];

        return render(request,'course-detail.html',{
            'course_detail':course_detail,
            'relate_course':relate_course
        })


class CourseInfoView(LoginRequiredMixin,View):
    #课程章节信息
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id));
        course.students +=1;
        course.save();

       #查询用户是否已经有学习该课程
        user_courses=UserCourse.objects.filter(user=request.user,course=course);
        if not user_courses:
            user_course=UserCourse(user=request.user,course=course);
            user_course.save();
        #获取相关课程
        user_coursers=UserCourse.objects.filter(course=course);
        user_ids=[ user_courser.user.id for user_courser in user_coursers];
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        #获取学过该课程的用户学习的其他课程
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        #获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resource= CourseResource.objects.filter(course=course)
        return render(request,'course-video.html',{
          'course':course,
         'relate_courses':relate_courses,
        'all_resource':all_resource

        })


class CommentsView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course=Course.objects.get(id=int(course_id));
        user_coursers=UserCourse.objects.filter(course=course);
        user_ids=[ user_courser.user.id for user_courser in user_coursers];
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        #获取学过该课程的用户学习的其他课程
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        #获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_comments=CourseComments.objects.all()
        all_resource= CourseResource.objects.filter(course=course)
        return render(request,'course-comment.html',{
              'course':course,
            'all_comments':all_comments,
            'all_resource':all_resource,
            'relate_courses':relate_courses

            })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) >0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class VideoPlayView(View):
    #视频播放
    def get(self,request,video_id):
        video=Video.objects.get(id=int(video_id));
        course=video.lesson.course;
        user_coursers=UserCourse.objects.filter(course=course);
        user_ids=[ user_courser.user.id for user_courser in user_coursers];
        all_user_courses=UserCourse.objects.filter(user_id__in=user_ids)
        #获取学过该课程的用户学习的其他课程
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        #获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_comments=CourseComments.objects.all()
        all_resource= CourseResource.objects.filter(course=course)
        return render(request,'course-play.html',{
              'course':course,
            'all_comments':all_comments,
            'all_resource':all_resource,
            'relate_courses':relate_courses,
            'video':video

            })

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xadmin
from .models import UserAsk,UserFavorite,UserMessage,CourseComments,UserCourse
from import_export import resources


# Register your models here.


class UserAskAdmin(object):
    pass


class UserFavoriteAdmin(object):
    pass


class UserMessageAdmin(object):
    pass


class UserCourseAdmin(object):
    pass


class CourseCommentsAdmin(object):
    pass

class UserFavoriteResource(resources.ModelResource):
    class Meta:
        model = UserFavorite
        fields = ('user', 'fav_id','fav_type','add_time')
        # exclude = ()
@xadmin.sites.register(UserFavorite)
class FooAdmin(object):
    import_export_args = {'import_resource_class': UserFavoriteResource}



xadmin.site.register(UserAsk,UserAskAdmin);
# xadmin.site.register(UserFavorite,UserFavoriteAdmin);
xadmin.site.register(CourseComments,CourseCommentsAdmin);
xadmin.site.register(UserMessage,UserMessageAdmin);

xadmin.site.register(UserCourse,UserCourseAdmin);
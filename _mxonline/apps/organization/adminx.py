#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xadmin
from .models import CityDict,CourseOrg,Teacher

class CityDictAdmin(object):
    pass


class CourseOrgAdmin(object):
    #搜索
    relfield_style='fk-ajax';
    style_fields = {"detail":"ueditor"}


class TeacherAdmin(object):
    pass


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)


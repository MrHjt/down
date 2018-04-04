#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xadmin
from xadmin import views


from .models import EmailVerifyRecord,Banner


class BaseSetting(object):
    enable_themes=True;
    use_bootswatch=True;


class GlobalSetting(object):
    site_title=u"后台管理系统";
    site_footer=u"慕雪在线网";
    menu_style="accordion"


class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time'];
    search_fields=['code','email','send_type','send_time'];
    list_filter=['code','email','send_type','send_time'];
    model_icon = 'fa fa-address-book-o';


class BannerAdmin(object):
    pass


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting);
xadmin.site.register(views.CommAdminView,GlobalSetting);


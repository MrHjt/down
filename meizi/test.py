#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request

thispic="http://mm.chinasareview.com/wp-content/uploads/2017a/08/02/01.jpg";
i=0;
localpath = "D:/_scrapy/meizi/meizi/image" + str(i) + ".jpg"
#通过urllib.request.urlretrieve()将原图片下载到本地
urllib.request.urlretrieve(thispic, filename=localpath)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
from urllib import request


url='https://www.douban.com/misc/captcha?id=I5Z5ewMlbVEKDIIueqvPjrci:en&size=s';
opener=request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
request.install_opener(opener)

#构造出图片在本地存储的地址

localpath = "D:/_scrapy/douban.com/tools/image/" +url+".jpg"
#通过urllib.request.urlretrieve()将原图片下载到本地
request.urlretrieve(url, filename=localpath)





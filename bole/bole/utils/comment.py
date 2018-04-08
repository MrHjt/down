#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import re

def get_md5(url):
    if isinstance(url,str):
        url=url.encode("utf-8");
    m=hashlib.md5(url);
    m.update(url);
    return m.hexdigest()

def get_nums(value):
    match_fav=re.match('.*?(\d+).*',value)
    if match_fav:
        nums=int(match_fav.group(1));
    else:
        nums=0;
    return nums

# if __name__=="__main__":
#
#     print(get_md5("http://blog.jobbole.com/all-posts/"))

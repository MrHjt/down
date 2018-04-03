#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

def get_md5(url):
    if isinstance(url,str):
        url=url.encode("utf-8");
    m=hashlib.md5(url);
    m.update(url);
    return m.hexdigest()

# if __name__=="__main__":
#
#     print(get_md5("http://blog.jobbole.com/all-posts/"))

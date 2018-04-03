#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
header = {
    "HOST":"www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': agent
}
def get_xsrf():
    #获取xsrf code
    response = requests.get("https://www.zhihu.com", headers=header)
    print(response.text)
    return ""
    # match_obj = re.match('.*name="_xsrf" value="(.*?)"', response.text)
    # if match_obj:
    #     return (match_obj.group(1))


def zhihu_login(account, password):
    #知乎登录
    if re.match("^1\d{10}",account):
        print ("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password
        }

get_xsrf().encode("utf-8")
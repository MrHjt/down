# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,FormRequest
import urllib
from urllib import request

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['douban.com']
    # start_urls = ['http://douban.com/']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0",
        "Accept"	:"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    def start_requests(self):
        url='https://www.douban.com/accounts/login'
        return [Request(url=url,headers=self.headers,callback=self.parse,meta={"cookiejar":1})]


    def parse(self, response):

        captcha=response.css(".captcha_image::attr(src)").extract()[0];
        if captcha:
            request.urlretrieve(captcha,filename='D:/_scrapy/douban.com/tools/image/test.jpg')
            captcha_code=input("input captcha....")
            data={
            "form_email":"1378556106@qq.com",
            "form_password":"tian1234",
            "login":"登陆",
            "captcha-solution":captcha_code
                 }
            print("Login.....")
        else:
            data={
            "form_email":"1378556106@qq.com",
            "form_password":"tian1234",
            "login":"登陆",
        }
            print("Login.....")
        return FormRequest.from_response(
            response,
            headers=self.headers,
            formdata=data,
            callback=self.show,
            meta={"cookiejar":response.meta["cookiejar"]}
            )

    def show(self,response):
        print(response.body)
        pass

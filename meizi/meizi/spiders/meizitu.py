# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from urllib import parse
from fake_useragent import UserAgent
import re


from meizi.items import MeiziItem


class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['www.meizitu.com']
    # start_urls = ['http://www.meizitu.com/']
    start_urls=['http://www.meizitu.com/a/more_1.html'];
    ua = UserAgent()
    headers = {'User-Agent': ua.random}




    def parse(self, response):
        post_urls=response.css("div.pic a::attr(href)").extract();
        for post in post_urls:
            yield Request(url=parse.urljoin(response.url,post),callback=self.ImageItem,headers=self.headers)


        for i in range(2,72):
            url='http://www.meizitu.com/a/more_'+str(i)+'.html'
            yield Request(url=url,callback=self.parse,headers=self.headers);


    def ImageItem(self,response):
        image_item=MeiziItem();
        if not "postContent" in response.text:
            image_item["imageurl"]=response.css("div#picture p img::attr(src)").extract()
        else:
            image_item["imageurl"]=response.css("div.postContent p img::attr(src)").extract()

        match_fav=re.match('.*?(\d+).*',response.url)
        image_item["url"]=match_fav;

        return image_item;


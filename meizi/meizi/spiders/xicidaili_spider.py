#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from fake_useragent import UserAgent
from meizi.items import XicidailiItem


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains=['www.xicidaili.com']
    # start_urls=['http://www.xicidaili.com/nn/1']
    ua = UserAgent()
    headers = {'User-Agent': ua.random}


    def start_requests(self):
        urls=[]
        for i in range(1,11):
            urls.append('http://www.xicidaili.com/nn/'+str(i))
        for url in urls:
            yield scrapy.Request(url,callback=self.parse,method='GET',headers=self.headers)

    def parse(self, response):
        tr_list=response.xpath('//table[@id="ip_list"]/tr')
        for tr in tr_list[1:]:  # 过滤掉表头行
            item=XicidailiItem()
            item['ip']=tr.xpath('./td[2]/text()').extract_first()
            item['port']=tr.xpath('./td[3]/text()').extract_first()
            item['type']=tr.xpath('./td[6]/text()').extract_first()
            item['speed']=tr.xpath('./td[7]/div/@title').re(r'\d{1,3}\.\d{0,}')[0]

            yield item
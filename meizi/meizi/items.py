# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeiziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    imageurl=scrapy.Field()
    url=scrapy.Field()
    pass


class XicidailiItem(scrapy.Item):
    # IP地址
    ip=scrapy.Field()
    # 端口号
    port=scrapy.Field()
    # 服务器地址
    # 类型
    type=scrapy.Field()
    # 速度
    speed=scrapy.Field()
    # 连接时间
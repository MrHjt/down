# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader import ItemLoader
import re

from scrapy.loader.processors import MapCompose,TakeFirst,Join


class BoleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def date_convert(value):
    try:
        create_date=datetime.datetime.strptime(value,"%Y/%m/%d").date();
    except Exception as e:
        create_date=datetime.datetime.now().date()
    return create_date


def get_nums(value):
    match_fav=re.match('.*?(\d+).*',value)
    if match_fav:
        nums=int(match_fav.group(1));
    else:
        nums=0;
    return nums

def remove_conmment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def return_value(value):
    return value






class JobbleArticleItem(scrapy.Item):
    title=scrapy.Field();
    create_date=scrapy.Field(
        input_processor=MapCompose(date_convert)
    );
    url=scrapy.Field();
    url_object_id=scrapy.Field()
    front_image_url=scrapy.Field(
        input_processor=MapCompose(return_value)
    );
    front_image_path=scrapy.Field()
    like_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    );
    fav_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    );
    comment_nums=scrapy.Field(
        input_processor=MapCompose(get_nums)
    );
    content=scrapy.Field();
    tag=scrapy.Field(
        input_processor=MapCompose(remove_conmment_tags),
        output_processor=Join(",")
    )


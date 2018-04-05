# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader import ItemLoader
import re
from w3lib.html import remove_tags


from bole.settings import SQL_DATE_FORMAT,SQL_DATETIME_FORMAT


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

class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

def replace_degress(value):
    value=value.replace("/","");
    return value


def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)


def hand_strip(value):
    return value.strip()


class LagouItem(scrapy.Item):
    url=scrapy.Field();
    url_object_id=scrapy.Field()
    title=scrapy.Field();
    salary=scrapy.Field();
    job_city=scrapy.Field(
         input_processor=MapCompose(replace_degress)
    );
    work_years=scrapy.Field(
        input_processor=MapCompose(replace_degress,handle_jobaddr)
    );
    degree_need=scrapy.Field(
        input_processor=MapCompose(replace_degress)
    );
    job_type=scrapy.Field();
    publish_time=scrapy.Field();
    job_advantags=scrapy.Field();
    job_dec=scrapy.Field(
        input_processor=MapCompose(hand_strip)
    );
    job_addr=scrapy.Field(
         input_processor=MapCompose(remove_tags,handle_jobaddr)
    );
    company_name=scrapy.Field();
    company_url=scrapy.Field();
    tags=scrapy.Field(
        input_processor=Join(","),
    )
    crawl_time=scrapy.Field();
    crawl_update_time=scrapy.Field();



    def get_insert_sql(self):
        insert_sql="""
        insert into logo_job(url,url_object_id,title,salary,job_city,work_years,degree_need,job_type,publish_time,
        job_advantags,job_dec,job_addr,company_name,company_url,tags,crawl_time)
       values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
       ON DUPLICATE KEY UPDATE salary=VALUES(salary), job_dec=VALUES(job_dec), job_addr=VALUES(job_addr)
        """
        params=(self["url"],self["url_object_id"],self["title"],self["salary"],self["job_city"],self["work_years"],self["degree_need"],
                self["job_type"],self["publish_time"],self["job_advantags"],self["job_dec"],self["job_addr"],self["company_name"],
                self["company_url"],self["tags"],self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
                )
        return insert_sql,params


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


class ZhihuQuestionItem(scrapy.Item):
    zhihu_id=scrapy.Field();
    topic=scrapy.Field();
    url=scrapy.Field();
    title=scrapy.Field();
    content=scrapy.Field();
    create_time=scrapy.Field();
    update_time=scrapy.Field();
    answer_num=scrapy.Field();
    comments_num=scrapy.Field();
    watch_user_num=scrapy.Field();
    click_num=scrapy.Field();
    crawl_time=scrapy.Field();

    def get_insert_sql(self):
        #插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_question(zhihu_id, topic, url, title, content, answer_num, commets_num,
              watch_user_num, click_num, crawl_time
              )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES(content), answer_num=VALUES(answer_num),
              watch_user_num=VALUES(watch_user_num), click_num=VALUES(click_num)
        """
        zhihu_id = int(self["zhihu_id"][0])
        topic = ",".join(self["topic"])
        url = self["url"][0]
        title = "".join(self["title"])
        content = "".join(self["content"])
        answer_num = get_nums("".join(self["answer_num"]))
        comments_num = get_nums("".join(self["comments_num"]))

        if len(self["watch_user_num"]) == 2:
            watch_user_num = int(self["watch_user_num"][0])
            # watch_user_num = int(re.sub("\D", "", self["watch_user_num"][0]))
            click_num = int(self["watch_user_num"][1])
        else:
            watch_user_num = int(self["watch_user_num"][0])
            # watch_user_num = int(re.sub("\D", "", self["watch_user_num"][0]))
            click_num = 0

        crawl_time = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (zhihu_id, topic, url, title, content, answer_num, comments_num,
                  watch_user_num, click_num, crawl_time)

        return insert_sql, params


class ZhihuAnwserItem(scrapy.Item):
    zhihu_id=scrapy.Field();
    url=scrapy.Field();
    question_id=scrapy.Field();
    author_id=scrapy.Field();
    content=scrapy.Field();
    praise_num=scrapy.Field();
    comments_num=scrapy.Field();
    create_time=scrapy.Field();
    update_time=scrapy.Field();
    crawl_time=scrapy.Field();

    def get_insert_sql(self):
        #插入知乎question表的sql语句
        insert_sql = """
            insert into zhihu_answer(zhuhu_id, url, question_id, author_id, content, praise_num, comment_num,
              create_time, update_time, crawl_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content=VALUES(content),  praise_num=VALUES(praise_num),
              update_time=VALUES(update_time)
        """

        create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["zhihu_id"], self["url"], self["question_id"],
            self["author_id"], self["content"], self["praise_num"],
            self["comments_num"], create_time, update_time,
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT),
        )

        return insert_sql, params


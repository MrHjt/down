# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

# from bole import settings

class BolePipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,values in results:
            image_file_path=values["path"];
        item["fron_image_path"]=image_file_path;
        return item


class JsonWithEncodeingPiepline(object):
    def __init__(self):
        self.file=codecs.open("article.json","w",encoding="utf-8")
    def process_item(self,item,spider):
        line=json.dumps(dict(item),ensure_ascii=False)+"\n";
        self.file.write(line);
        return item
    def spider_closed(self,spider):
        self.file.close()

class MysqlPipeline(object):
    #采用同步机制写入MySQL
    def __init__(self):
        self.conn=MySQLdb.connect("localhost","root","123456","scrapy",charset="utf8",use_unicode=True);
        self.cursor=self.conn.cursor();
    def process_item(self,item,spider):
        sql="""
        insert into bole(title,url_object_id,url,create_date,fav_nums) values (%s,%s,%s,%s,%s)
        """
        self.cursor.execute(sql,(item["title"],item["url_object_id"],item["url"],item["create_date"],item["fav_nums"]));
        self.conn.commit()


class Mysql_TwistedPipeline(object):
    def __init__(self,dbpool):
        self.dbpool=dbpool;

    @classmethod
    def from_setting(cls,settings):

        dbparms=dict(
            host=settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool=adbapi.ConnectionPool("MySQLdb",**dbparms);

        return cls(dbpool)

    def process_item(self,item,spider):
        #使用twisted将MySQL插入变成异步执行
        query=self.dbpool.runInteraction(self.do_insert,item);
        query.addErrback(self.handle_error,item,spider)

    def handle_error(self,failure,item,spider):
        print(failure)

    def do_insert(self,cursor,item):
        #根据不同的item构建不同的sql语句并插入MySQL中
        insert_sql,params=item.get_insert_sql()

        print(insert_sql,params);
        cursor.execute(insert_sql,params);


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        # print (insert_sql, params)
        cursor.execute(insert_sql, params)









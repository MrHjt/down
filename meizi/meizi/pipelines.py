# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from urllib import request
from random import Random
import pymysql
import MySQLdb


class MeiziPipeline(object):
    def process_item(self, item, spider):
        for i in range(0,len(item["imageurl"])):
		#生成随意序列
            st = ''
            chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
            length = len(chars) - 1
            random = Random()
            for i in range(7):
                st+=chars[random.randint(0, length)]
				
			#伪造请求
            opener=request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36')]
            request.install_opener(opener)
            thispic=item["imageurl"]
            print(thispic)
#构造出图片在本地存储的地址
            root=str(item["url"])+"-"+str(i);
            localpath = "D:/_scrapy/meizi/meizi/images/" +st+".jpg"
#通过urllib.request.urlretrieve()将原图片下载到本地
            request.urlretrieve(thispic, filename=localpath)
        return item


class XicidailiPipeline(object):
    """
    西刺代理爬虫 item Pipeline

    create table xicidaili(
        id int primary key auto_increment,
        country varchar(10) not null,
        ip varchar(30) not null,
        port varchar(10) not null,
        address varchar(30) not null,
        anonymous varchar(10) not null,
        type varchar(20) not null,
        speed varchar(10) not null,
        connect_time varchar(20) not null,
        alive_time varchar(20) not null,
        verify_time varchar(20) not null);
    """
    def __init__(self):
        self.conn=MySQLdb.connect("localhost","root","123456","scrapy",charset="utf8",use_unicode=True);
        self.cursor=self.conn.cursor();
    def process_item(self,item,spider):
        sql="""
        insert into proxy_ip(ip,port,type,speed) values (%s,%s,%s,%s)
        """
        self.cursor.execute(sql,(item['ip'],item['port'],'https',item['speed']));
        self.conn.commit()

    def close_spider(self,spider):
        self.conn.close()

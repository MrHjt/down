#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from scrapy.selector import Selector
import MySQLdb


conn=MySQLdb.connect("localhost","root","123456","scrapy",charset="utf8",use_unicode=True);
cursor=conn.cursor();
# def crawl_ips():
#     headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",}
#     for i in range(2500):
#         re=requests.get("http://www.xicidaili.com/nn/{0}".format(i),headers=headers);
#
#     ip_list=[]
#     selector=Selector(text=re.text);
#     all_trs=selector.css("#ip_list tr")
#     for all_tr in all_trs:
#         speed_str=all_tr.css(".bar::attr(title)").extract();
#         if speed_str:
#             speed=float(speed_str.split("秒")[0])
#         all_text=all_tr.css("td::text").extract()
#         ip=all_text[0];
#         port=all_text[1];
#         proxy_type=all_text[5];
#         ip_list.append((ip,port,proxy_type,speed));
#
#         for ip_info in ip_list:
#             cursor.execute("insert into proxy_ip(ip,port,speed,type) values ('{0}','{1}','{2}','https'')".format(ip_info[0],ip_info[1],ip_info[3]))
#             conn.commit()
#
#
# crawl_ips()

class GetIp():
    def delete_ip(self,ip):
        sql="""
        delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(sql);
        conn.commit();
        return True;


    def judge_ip(self,ip,port):
        http_url="http://www.baidu.com";
        proxy_url="http://"+ip+":"+port;
        try:
            proxu_dict={
            "https":proxy_url}
            response=requests.get(http_url,proxies=proxu_dict);
        except Exception as e:
            print("invalid ip ans port");
            self.delete_ip(ip);
            return False
        else:
            code=response.status_code;
            if code>=200 and code<300:
                print("effective ip")
                return True
            else:
                print("invalid ip ans port");
                self.delete_ip(ip);
                return False


    def get_random_ip(self):
        sql=""" select ip,port from proxy_ip order by rand() limit 1
                """
        result=cursor.execute(sql);
        for ip_info in cursor.fetchall():
            ip=ip_info[0];
            port=ip_info[1];
            judge_re=self.judge_ip(ip,port)
            if judge_re:
                return "http://"+ip+":"+port;
            else:
                self.get_random_ip()


t=GetIp();
y=t.get_random_ip();
print(y)
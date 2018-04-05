# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bole.items import ItemLoader
from bole.items import LagouItem
from bole.items import LagouItemLoader
import datetime

from bole.utils.comment import get_md5


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('https://www.lagou.com/zhaopin/Python')),follow=True),
    )

    def parse_item(self, response):
        lagou_item = LagouItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item_loader=LagouItemLoader(item=LagouItem(),response=response);
        item_loader.add_css("title","div.job-name span.name::text");
        item_loader.add_value("url",response.url);
        item_loader.add_value("url_object_id",get_md5(response.url));
        item_loader.add_css("salary","dd.job_request p span.salary::text");
        item_loader.add_xpath("job_city","//dd[@class='job_request']/p[1]/span[2]/text()");
        item_loader.add_xpath("work_years","//dd[@class='job_request']/p[1]/span[3]/text()");
        item_loader.add_xpath("degree_need","//dd[@class='job_request']/p[1]/span[4]/text()");
        item_loader.add_xpath("job_type","//dd[@class='job_request']/p[1]/span[5]/text()");
        item_loader.add_css("publish_time",".publish_time::text");
        item_loader.add_css("job_advantags",".job-advantage p::text");
        item_loader.add_css("job_dec",".job_bt div");
        item_loader.add_css("job_addr",".work_addr");
        item_loader.add_css("company_name",".job_company dt a img::attr(alt)");
        item_loader.add_css("company_url",".job_company dt a::attr(href)");
        item_loader.add_css("tags",'ul.position-label li::text'),
        item_loader.add_value('crawl_time', datetime.datetime.now().date())

        lagou_item=item_loader.load_item()

        return lagou_item

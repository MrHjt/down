# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
import datetime
from urllib import parse
from scrapy.loader import ItemLoader


from bole.items import JobbleArticleItem,ArticleItemLoader
from bole.utils.comment import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        post_nodes=response.css("#archive .floated-thumb .post-thumb a");
        for post_node in post_nodes:
            post_url=post_node.css("::attr(href)").extract_first();
            image_url=post_node.css("img::attr(src)").extract_first()
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":image_url},callback=self.parse_detail)

        next_url=response.css(".next.page-numbers::attr(href)").extract_first("");
        if next_url:
             yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)



    def parse_detail(self,response):
        article_item=JobbleArticleItem()

        # title=response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")[0];
        # # create_date=response.xpath('//*[@id="post-113728"]/div[2]/p/text()[1]').extract_first()[0].strip().replace("·","").strip()
        # create_date=response.xpath('//*[@class="entry-meta-hide-on-mobile"]/text()').extract_first()[0].strip().replace("·","").strip()
        #
        # like_num=int(response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract_first()[0])
        # fav_nums= response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()[0];
        # match_fav=re.match('.*?(\d+).*',fav_nums)
        # if match_fav:
        #     fav_nums=int(match_fav.group(1));
        # else:
        #     fav_nums=0;
        # comment_nums= response.xpath("//a[@href='#article-comment']/span/text()").extract_first()[0];
        # match_fav=re.match('.*？(\d+).*',comment_nums)
        # if match_fav:
        #     comment_nums=int(match_fav.group(1));
        # else:
        #     comment_nums=0;
        #
        # content=response.xpath("//div[@class='entry']").extract_first()[0];
        #
        # # create=response.xpath('//*[@class="entry-meta-hide-on-mobile"]/a/text()').extract_first()[0]
        #
        # tag_list=response.xpath('//*[@class="entry-meta-hide-on-mobile"]/a/text()').extract_first()
        #
        # tag_list=[element for element in tag_list if not element.strip().endswith("评论")];
        #
        # tag_list=','.join(tag_list);


        #利用css选择器提取信息
        #封面图
        # front_image_url=response.meta.get("front_image_url","")
        # title=response.css(".entry-header h1::text").extract()[0];
        # create_date= response.css("p.entry-meta-hide-on-mobile::text").extract()[0].strip().replace("·","").strip()
        #
        # try:
        #     create_date=datetime.datetime.strptime(create_date,"%Y/%m/%d").date();
        # except Exception as e:
        #     create_date=datetime.datetime.now().date()
        #
        # like_nums=response.css(".vote-post-up h10::text").extract()[0];
        # fav_nums=response.css(".bookmark-btn::text").extract()[0];
        # match_fav=re.match('.*?(\d+).*',fav_nums)
        # if match_fav:
        #     fav_nums=int(match_fav.group(1));
        # else:
        #     fav_nums=0;
        #
        # comment_nums=response.css('a[href="#article-comment"] span ::text').extract()[0];
        # match_fav=re.match('.*?(\d+).*',comment_nums)
        # if match_fav:
        #     comment_nums=int(match_fav.group(1));
        # else:
        #     comment_nums=0;
        #
        # content=response.css("div.entry").extract()[0];
        # tag_list=response.css('.entry-meta-hide-on-mobile a::text').extract()
        #
        # tag_list=[element for element in tag_list if not element.strip().endswith("评论")];
        #
        # tag_list=','.join(tag_list);
        #
        #
        # article_item["title"]=title;
        # article_item["url"]=response.url;
        # article_item["create_date"]=create_date;
        # article_item["like_nums"]=like_nums;
        # article_item["fav_nums"]=fav_nums;
        # article_item["comment_nums"]=comment_nums;
        # article_item["tag"]=tag_list;
        # article_item["content"]=content;
        # article_item["front_image_url"]=[front_image_url];
        # article_item["url_object_id"]=get_md5(response.url);


        front_image_url=response.meta.get("front_image_url","")
        item_loader=ArticleItemLoader(item=JobbleArticleItem(),response=response);
        item_loader.add_css("title",".entry-header h1::text");
        item_loader.add_css("create_date","p.entry-meta-hide-on-mobile::text");
        item_loader.add_value("url",response.url);
        item_loader.add_value("url_object_id",get_md5(response.url));
        item_loader.add_value("front_image_url",[front_image_url]);
        item_loader.add_css("like_nums",".vote-post-up h10::text");
        item_loader.add_css("fav_nums",".bookmark-btn::text");
        item_loader.add_css("comment_nums",'a[href="#article-comment"] span ::text');
        item_loader.add_css("tag",".entry-meta-hide-on-mobile a::text");
        item_loader.add_css("content","div.entry");

        article_item=item_loader.load_item()



        yield article_item



from django.db import models

# Create your models here.
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text,Integer
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class ArticlePost(DocType):
    suggest=Completion(analyzer=ik_analyzer)
    title=Text(analyzer='ik_max_word' );
    create_date=Date();
    url=Keyword();
    url_object_id=Keyword();
    front_image_url=Keyword();
    front_image_path=Keyword();
    like_nums=Integer();
    fav_nums=Integer();
    comment_nums=Integer();
    content=Text(analyzer='ik_max_word' );
    tag=Text(analyzer='ik_max_word' );


    class Meta:
        index="jobbole";
        doc_type="article"



    # ArticlePost.init()


class LagouItem(DocType):
    suggest=Completion(analyzer=ik_analyzer)
    url=Keyword();
    url_object_id=Keyword();
    title=Text(analyzer='ik_max_word' );
    salary=Keyword();
    job_city=Keyword();
    work_years=Keyword();
    degree_need=Keyword();
    job_type=Keyword();
    publish_time=Date()
    job_advantags=Text(analyzer='ik_max_word' );
    job_dec=Text(analyzer='ik_max_word' );
    job_addr=Keyword();
    company_name=Keyword();
    company_url=Keyword();
    tags=Text(analyzer='ik_max_word' );
    crawl_time=Date();
    crawl_update_time=Date();

    class Meta:
        index="lagou";
        doc_type="job"



class ZhihuQuestionItem(DocType):
    suggest=Completion(analyzer=ik_analyzer)
    zhihu_id=Keyword();
    topic=Keyword();
    url=Keyword();
    title=Text(analyzer='ik_max_word' );
    content=Text(analyzer='ik_max_word' );
    create_time=Date();
    update_time=Date();
    answer_num=Integer();
    comments_num=Integer();
    watch_user_num=Integer();
    click_num=Integer();
    crawl_time=Date();

    class Meta:
        index="zhihu";
        doc_type="question"



class ZhihuAnwserItem(DocType):
    suggest=Completion(analyzer=ik_analyzer)
    zhihu_id=Keyword();
    url=Keyword();
    question_id=Keyword();
    author_id=Keyword();
    content=Text(analyzer='ik_max_word' );
    praise_num=Integer();
    comments_num=Integer();
    create_time=Date();
    update_time=Date();
    crawl_time=Date();


    class Meta:
        index="zhihu";
        doc_type="answer"

if __name__=="__main__":
    LagouItem.init()
    ZhihuQuestionItem.init();
    ZhihuAnwserItem.init();

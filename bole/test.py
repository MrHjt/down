#!/usr/bin/env python
# -*- coding: utf-8 -*-
tag_list=['业界', ' 2 评论 ', '开源']
tag_list=[element for element in tag_list if not element.strip().endswith("评论")];
tag_list=','.join(tag_list);
print(tag_list)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from time import sleep



#无图加载#设置
# chrom_opt=webdriver.ChromeOptions();
# prefs={"profile.managed_default_content_settings.images":2};
# chrom_opt.add_experimental_option("prefs",prefs);
#
# browser=webdriver.Chrome(executable_path="D:/_scrapy/chromedriver.exe",chrome_options=chrom_opt);
url="https://www.zhihu.com";


browser=webdriver.PhantomJS(executable_path="D:/_scrapy/phantomjs-2.1.1-windows/bin/phantomjs.exe");
s = requests.Session()

s.headers.clear()#清除requests头部中的Python机器人信息，否则登录失败

browser.get("https://weibo.com/");
sleep(15);
# browser.find_element_by_css_selector("#loginname").send_keys("18606941891");
# browser.find_element_by_css_selector("div.info_list.password input[node-type='password']").send_keys("3259768703");
# browser.find_element_by_css_selector("div.info_list.login_btn a.W_btn_a.btn_32px").click()
# #
# #获取源码
print(browser.page_source)
browser.quit()
# # browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
# browser.find_element_by_css_selector("div.SignFlow-accountInput.Input-wrapper input[name='username']").send_keys("18639435990");
# browser.find_element_by_css_selector("div.SignFlowInput div.Input-wrapper input[name='password']").send_keys("3259768703");
# sleep(10)
# browser.find_element_by_css_selector("button.Button SignFlow-submitButton").submit()

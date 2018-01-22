#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################################################################################################
# 基金估值：http://fundgz.1234567.com.cn/js/160222.js?rt=1516587368315
# 基金详细信息：http://fund.eastmoney.com/pingzhongdata/160222.js?v=20180122095601
# 代码借鉴了以下文章：http://blog.csdn.net/yuzhucu/article/details/55261024
#######################################################################################################

__author__ = 'DouBa'

import requests  
from bs4 import BeautifulSoup  
import time  
import random  
import pymysql  
import os  
import pandas as pd  
import re

def randHeader():  
    # 随机生成User-Agent     
    head_connection = ['Keep-Alive', 'close']  
    head_accept = ['text/html, application/xhtml+xml,application/xml, */*']  
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']  
    head_user_agent = ['Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',  
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',  
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',  
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',  
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',  
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',  
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',  
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',  
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',  
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',  
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',  
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',  
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',  
                       'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',  
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0'  
                       ]  
    result = {  
        'Connection': head_connection[0],  
        'Accept': head_accept[0],  
        'Accept-Language': head_accept_language[1],  
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]  
    }  
    return result  

def get_html_soup(url):#获取解编码后的HTML
    html = None
    try:        
        header = {'Host': 'fund.eastmoney.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
          'Connection': 'keep-alive'}
        req = request.Request(url,headers=header)
        response = request.urlopen(req, timeout = 100)
        html = response.read().decode(encoding = "utf-8", errors='ignore')
    except Exception as e:
        print(e, "please check your network situation")
        return None
    soup = BeautifulSoup(str(html), "lxml")    
    return soup

def page_url(url, page_num):#生成带页面的URL
    if page_num == 1:
        return url
    index = url.rfind(".")
    return url[0 : index] + "_" + str(page_num) + url[index : ]

def get_title_link(url, pattern):#获取新闻的标题和正文链接
    soup = get_html_soup(url)
    news_link = {}

    scroll_list1 = BeautifulSoup(str(soup.find("div", attrs = pattern)), "lxml")
    scroll_list = BeautifulSoup(str(scroll_list1.find_all("h2")), "lxml")
    for link in scroll_list.find_all("a"):    
        if len(link.get_text().strip()) > 0 and link.get("href").find("http") != -1:
            news_link[link.get_text().strip()] = link.get('href')
    return news_link

def get_intraday_valuation(url, pattern):#抓取盘中估值
    soup= get_html_soup(url)
    intraday_valuation = BeautifulSoup(str(soup.find("dl",attrs=pattern)),"lxml")    
    string = "估值:"+intraday_valuation.find(id="gz_gsz").getText().strip()
    string += ",涨跌:"+intraday_valuation.find(id="gz_gszze").getText().strip()
    string += ","+intraday_valuation.find(id="gz_gszzl").getText().strip()
    return string

def get_news_body(url):#抓取新闻主体内容
    first = True
    content_text = []
    page_num = 1
    article_div = ""

    #使用循环处理有分页的新闻
    while first == True or article_div.find("下一页</a>") != -1:
        soup = get_html_soup(page_url(url, page_num))
        if soup == None:
            return None

        #article_div = str(soup.find("div", attrs = {"class": "article"}))
        article_div = str(soup.find("div", attrs = {"class": "news_info"}))
        soup = BeautifulSoup(str(article_div), "lxml")
        for content in soup.find_all("p"):
            if len(content.get_text().strip()) > 0:
                content_text.append(" " + content.get_text().strip())
        page_num += 1
        first = False
    for x in content_text:
        if x == " None":
            return None
    return content_text

def clean_chinese_character(text):
    '''处理特殊的中文符号,将其全部替换为'-' 否则在保存时Windows无法将有的中文符号作为路径'''
    chars = chars = ["/", "\"", "'", "·", "。","？", "！", "，", "、", "；", "：", "‘", "’", "“", "”", "（", "）", "…", "–", "．", "《", "》"];
    new_text = ""
    for i in range(len(text)):
        if text[i] not in chars:
            new_text += text[i]
        else:
            new_text += "_"
    return new_text;
########################################################################

code_url = "http://fund.eastmoney.com/160222.html"

#html = etree.HTML(data)
#td = html.xpath('//div[@class="feed-section"]/:text()')
#code_url_pattern = {"id": "main"}
code_url_pattern = {"class": "dataItem01"}

#获取盘中估值
new_str = get_intraday_valuation(code_url, code_url_pattern)
print(new_str)

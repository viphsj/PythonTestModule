#!/usr/bin/python3
# -*- coding: utf-8 -*-

'a test module'

__author__ = 'viphsj'

from urllib import request
import os
import shutil
from bs4 import BeautifulSoup

national = "国内"
international = "国际"

def get_html_soup(url):#获取解编码后的HTML
    html = None
    try:
        response = request.urlopen(url, timeout = 10)
        html = response.read().decode(encoding = "utf8", errors='ignore')
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

    scroll_list = BeautifulSoup(str(soup.find("div", attrs = pattern)), "lxml")    
    for link in scroll_list.find_all("a"):
        if len(link.get_text().strip()) > 0 and link.get("href").find("http") != -1:
            news_link[link.get_text()] = link.get('href')
    return news_link

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
        article_div = str(soup.find("div", attrs = {"class": "main"}))
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
#def create_docx(news_type, title, content):
#    '''这里使用python-docx库将新闻的内容生成word文件'''
#    document = Document()
#    paragraph = document.add_paragraph(title)
#    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
#    paragraph.bold = True
#
#    for x in content:
#        paragraph = document.add_paragraph(x)
#
#    style = paragraph.style
#    font = style.font
#    font.size = Pt(15)
#    font.name = "consolas"
#
#    name = news_type + "-" + clean_chinese_character(title) + ".docx"
#    document.save(news_type + "/" + name)
#
########################################################################
national_news = "http://blog.mydrivers.com/"
national_news_pattern = {"id": "main"}

#international_news = "http://www.news.cn/world/"
#international_news_pattern = {"class": "partR domPC"}

#获取新闻的标题和链接
national_news = get_title_link(national_news, national_news_pattern)
print("\ngetting national news content")
#获取新闻的内容主体并写入文件
for x in national_news:
    paras = get_news_body(national_news[x])
    #paras = get_news_body(x)
    if paras != None and len(paras) > 0:
        print ("writing:", clean_chinese_character(x), national_news[x])
        print ( x, paras)

print("All done, have a nice day")

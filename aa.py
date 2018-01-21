# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

soup = BeautifulSoup(open("1.html"),"lxml")
scroll_list = BeautifulSoup(str(soup.find("div", id="main")), "lxml")
link = scroll_list.find_all("a")
print(link)
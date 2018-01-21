#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Michael Huang'

from urllib import request
from lxml import etree

req = request.Request('http://www.douban.com')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
#    print('Data:', f.read().decode('utf-8'))
data = request.urlopen(req).read().decode('utf-8')
html = etree.HTML(data)
td = html.xpath('//div[@class="feed-section"]/:text()')
#area = td.text.content
#print ('Num',data)
print (type(td))
print (type(td[0]).xpath('string(.)'))
#for e in td:
 #   print(e.xpath('string(.)'))
 
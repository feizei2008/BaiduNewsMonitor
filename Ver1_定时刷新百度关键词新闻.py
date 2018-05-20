# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 19:33:29 2017

@author: zack zhang

实现功能：
    1、requests和bs4实现抓取和解析某一静态时点、单一关键词的百度新闻结果
    2、定时循环任务
存在问题：
    1、静态时点，无法实时监控新闻
    2、未实现多关键词轮询
    3、新闻来源信息解析失败
    4、requests.get()方法因输入的百度新闻参数不全，得到的新闻查询结果只有10条，不完整。
       非requests问题，是新闻链接参数不完善导致的。       
尝试方案：

"""
#import tushare as ts
#from threading import Timer
#
#def sinanews(): 
#  print ts.get_latest_news(top=9) 
#  t = Timer(10, sinanews) 
#  t.start() 
#    
#if __name__ == "__main__": 
#  sinanews()      
  
#http://blog.csdn.net/whiterbear/article/details/50232637

import requests
from bs4 import BeautifulSoup
from threading import Timer
import tushare as ts

StockList = ts.get_stock_basics().name
#StockName = StockList.name.tolist()
#print [i.decode('utf-8') for i in StockName]
print StockList
 
query_word = '李克强'    
news_base_url = 'http://news.baidu.com/ns?tn=news'

news_url = news_base_url + query_word
parameters = {'word': query_word}

# 获取 JSON 数据
r = requests.get(news_base_url, params=parameters)
print r.url

soup = BeautifulSoup(r.text, 'lxml')
news_html_list = soup.select('div.result')
news_list = []
#print news_html_list

for news_html in news_html_list:
    news = {}
    news['标题'] = news_html.a.get_text().strip()
    news['链接'] = news_html.a['href']
#    source = news_html.find('p', 'c-author').get_text().strip().replace('\xa0\xa0', ' ').split(' ')
#    news['来源'] = source[0]
#    news['发布日期'] = source[1]
    
    news_list.append(news)

def NewsMonitor():
    for news in news_list:
        for k, v in news.items():
            print k.decode('utf-8'), v
    t = Timer(10,NewsMonitor)
    t.start()
   
#if __name__ == "__main__": 
#  NewsMonitor()  



    
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 19:33:29 2017

@author: zack zhang

实现功能：
    1、requests和bs4实现抓取和解析某一静态时点、单一关键词的百度新闻结果
    2、定时循环任务
    3、实现python.exe在cmd下运行字体带颜色
    4、新闻来源信息解析成功
    5、实现cmd下运行新闻标题Title带颜色，来源Source不带颜色
    6、直接打印dic.vales而非dic的key、value,节省空间
    7、初步实现多关键词轮询
存在问题：
    1、requests.get()方法因输入的百度新闻参数不全，得到的新闻查询结果只有10条，不完整。
       非requests问题，是新闻链接参数不完善导致的。    
尝试方案：
    1、用ghost.py（须pip安装Ghost.py非ghost.py）模拟用户浏览网页习惯，
       以解决js异步返回（疑似）、ajax等导致的抓取网页内容不完整问题，
       但模拟用户浏览网页比较耗资源。且最终模块使用失败。
    2、用urllib2抓取网页，失败
    3、用list的sorted方法对新闻按时间排序，
       但无法解决“2017年11月24日09:45”和“6小时前”不同格式的时间排序问题
    
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

# -----------------colorama模块的一些常量---------------------------  
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.  
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.  
# Style: DIM, NORMAL, BRIGHT, RESET_ALL  
#  
  
from colorama import  init, Fore, Back, Style  
init(autoreset=True)  
class Colored(object):  
  
    #  前景色:红色  背景色:默认  
    def red(self, s):  
        return Fore.RED + s + Fore.RESET  
  
    #  前景色:绿色  背景色:默认  
    def green(self, s):  
        return Fore.GREEN + s + Fore.RESET  
  
    #  前景色:黄色  背景色:默认  
    def yellow(self, s):  
        return Fore.YELLOW + s + Fore.RESET  
  
    #  前景色:蓝色  背景色:默认  
    def blue(self, s):  
        return Fore.BLUE + s + Fore.RESET  
  
    #  前景色:洋红色  背景色:默认  
    def magenta(self, s):  
        return Fore.MAGENTA + s + Fore.RESET  
  
    #  前景色:青色  背景色:默认  
    def cyan(self, s):  
        return Fore.CYAN + s + Fore.RESET  
  
    #  前景色:白色  背景色:默认  
    def white(self, s):  
        return Fore.WHITE + s + Fore.RESET  
  
    #  前景色:黑色  背景色:默认  
    def black(self, s):  
        return Fore.BLACK  
  
    #  前景色:白色  背景色:绿色  
    def white_green(self, s):  
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET  
  
color = Colored()  
#print color.red('I am red!')  
#print color.green('I am gree!')  
#print color.yellow('I am yellow!')  
#print color.blue('I am blue!')  
#print color.magenta('I am magenta!')  
#print color.cyan('I am cyan!')  
#print color.white('I am white!')  
#print color.white_green('I am white green!')  

import requests
from bs4 import BeautifulSoup
from threading import Timer
import os
import tushare as ts
import collections

#StockList = ts.get_stock_basics().name
#StockName = StockList.name.tolist()
#print [i.decode('utf-8') for i in StockName]
#print StockList
 
#query_word = '刘涛'    
#news_base_url = 'http://news.baidu.com/ns?tn=news'

#news_url = news_base_url + query_word
#parameters = {'word': query_word}

# 获取 JSON 数据
#r = requests.get(news_base_url, params=parameters)
#print r.url

#soup = BeautifulSoup(r.text, 'lxml')
#news_html_list = soup.select('div.result')
#news_list = []
#print type(news_html_list[0]) 类型为：<class 'bs4.element.Tag'>
#k = news_html_list[0]
#news = {} 
#news['标题'] = k.a.get_text().strip()
#news['链接'] = k.a['href']
#news['来源时间'] = k.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')#.split(' ') #split把str切分成了list
#print k
#print "="*80
#print news['标题'], type(news['标题'])
#print "+"*50
#
#print news['链接'], type(news['链接'])
#print "+"*50
#
#print news['来源时间'], type(news['来源时间'])
#print news['来源时间'][-2:]
#print news
#for k, v in news.items():
#    if k is '标题':
#        print k.decode('utf-8'), color.red(v)
#    else:
#        print k.decode('utf-8'), v


        
#for news_html in news_html_list:
#    news = {}
#    news['Source+Title'] = news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ') + "__" +news_html.a.get_text().strip() 
##    news['链接'] = news_html.a['href']
##    news['来源时间'] = news_html.find('p', 'c-author').get_text().strip()
##    news['Source'] = news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')#.split(' ')
##    source = news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ').split(' ')
##    news['来源'] = source[0] + source[-2] + source[-1]
##    news['发布日期'] = source[-2]
##    news['发布时间'] = source[-1]
##    news['DateTime'] = source[-2] + source[-1]
#                     
#    news_list.append(news)

#sorted_news_list = sorted(news_list, key = lambda k: k['DateTime'], reverse=True )
                    
#for news in news_list:
#    for i in news.values():
#        print i
#    for k,v in news.iteritems():
#        print k.decode('utf-8'), v
#def NewsGrabber(query_word = '百慕大'):
#    news_base_url = 'http://news.baidu.com/ns?tn=news'
#    parameters = {'word': query_word}
#    r = requests.get(news_base_url, params=parameters)
#    soup = BeautifulSoup(r.text, 'lxml')
#    news_html_list = soup.select('div.result')
#    news_list = []
#    for news_html in news_html_list:
#        news = {}
#        news['Source+Title'] = news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ') + "__" +news_html.a.get_text().strip()
#        news_list.append(news)
#    return news_list

#print NewsGrabber(query_word = '百慕大')
                                       
#def NewsMonitor(query_word = '习近平'):
#    news_base_url = 'http://news.baidu.com/ns?tn=news'
#    parameters = {'word': query_word}
#    r = requests.get(news_base_url, params=parameters)
#    soup = BeautifulSoup(r.text, 'lxml')
#    news_html_list = soup.select('div.result')
#    news_list = []
#    for news_html in news_html_list:
#        news = {}
#        news['Source+Title'] = news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ') + "__" +news_html.a.get_text().strip()
#        news_list.append(news)
#        for news in news_list[:4]:
#            for i in news.values():
#                print i
#        for k, v in news.items():
#            if k is 'Title':#不知道为什么用“标题”就出错用“Title”就没问题
##                print "确实是Title"
##            else:
##                print "妈的错了！"
#                print color.yellow(k.decode('utf-8')), color.white_green(v)
#            else:
#                print k.decode('utf-8'), v                 
##        print "_"*15
#        print "*"*50    
#    t = Timer(10,NewsMonitor)
#    t.start()
path = os.path.abspath(os.path.dirname(__file__))
File = path+'\query-words.txt'
Rows = open(File).read().splitlines()

def NewsMonitor():
    query_words = Rows
    news_base_url = 'http://news.baidu.com/ns?tn=news'
    for word in query_words: 
        parameters = {'word': word}
        r = requests.get(news_base_url, params=parameters) #只能取到部分新闻！非源代码完整内容
        soup = BeautifulSoup(r.text, 'lxml')
        news_html_list = soup.select('div.result', limit = 3)#表示是3条新闻
#        news_list = []  #放在这里会造成新闻重复！！！      
        for news_html in news_html_list:
            news = {}
            news_list = []
#            news['Title'] = news_html.a.get_text().strip() 
            news['Title+Source'] = news_html.a.get_text().strip() + "--" + news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')
            news_list.append(news)#append方法和list要放在同一级，不然会发生list元素重复！！            
            for news in news_list:
                for i in news.values():
                    print i
    print "*"*50
    t = Timer(15,NewsMonitor)
    t.start()
    
if __name__ == "__main__": 
    NewsMonitor()  
#中断ipython执行是Ctrl+D

'''
目标1：多个关键词实现轮询
目标2：每条新闻之间更美观整洁
目标3：按新闻时间先后排序，但“2017年11月24日09:45”和“6小时前”不同格式的时间如何排？
'''


    
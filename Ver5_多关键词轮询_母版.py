# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 09:12:45 2017

@author: zack zhang

实现功能：
    1、requests和bs4实现抓取和解析某一静态时点、单一关键词的百度新闻结果
    2、定时循环任务
    3、实现python.exe在cmd下运行字体带颜色
    4、新闻来源信息解析成功
    5、实现cmd下运行新闻标题Title带颜色，来源Source不带颜色
存在问题：
    1、静态时点，无法实时监控新闻
    2、未实现多关键词轮询
    3、requests.get()方法因输入的百度新闻参数不全，得到的新闻查询结果只有10条，不完整。
       非requests问题，是新闻链接参数不完善导致的。    
尝试方案：
    1、用ghost.py（须pip安装Ghost.py非ghost.py）模拟用户浏览网页习惯，
       以解决js异步返回（疑似）、ajax等导致的抓取网页内容不完整问题，
       但模拟用户浏览网页比较耗资源。且最终模块使用失败。
    2、用urllib2抓取网页，失败
    

""" 

import requests
from bs4 import BeautifulSoup
from threading import Timer
import os
from ghost import Ghost
from requests.cookies import RequestsCookieJar

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
import urllib
path = os.path.abspath(os.path.dirname(__file__))
File = path+'\query-words.txt'
Rows = open(File).read().splitlines()


baseUrl = 'http://news.baidu.com/ns'
query_words = Rows
news_base_url = 'http://news.baidu.com/ns?tn=news'
parameters = {'word': '习近平'}
data = {'word': '习近平', 'pn=': str(8 - 1) + '0', 'cl': '2', 'ct': '1', 'tn': 'news', 'rn': '20',
                    'ie': 'utf-8', 'bt': 0, 'et': 0}
data = urllib.urlencode(data)
url = baseUrl + '?' + data
html = requests.get(url)
soup = BeautifulSoup(html.text, 'lxml')
news_html_list = soup.select('div.result')#, limit = 5表示是5条新闻
for news_html in news_html_list:
    news = {}
    news_list = []
    news['Title'] = news_html.a.get_text().strip() 
#        news['Title+Source'] = news_html.a.get_text().strip() + "--" + news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')
    news_list.append(news)#append方法和list要放在同一级，不然会发生list元素重复！！            
    for news in news_list:
        for i in news.values():
            print color.yellow(i)  


#ghost = Ghost()
#cj = RequestsCookieJar()
#with ghost.start() as session:
#    session.delete_cookies()
#    page, extra_resources = session.open(news_base_url, timeout=30)
#    session.save_cookies(cj)
#s = requests.Session()
#r = s.get(news_base_url, params=parameters, cookies=cj)
#print r.text

#import urllib2
#content = urllib2.urlopen('https://www.baidu.com/'+'上海').read() 
#
#print content
#soup = BeautifulSoup(content, 'lxml')
#news_html_list = soup.select('div.result')#, limit = 5表示是5条新闻
#print news_html_list

#for news_html in news_html_list:
#    news = {}
#    news_list = []
#    news['Title'] = news_html.a.get_text().strip() 
##        news['Title+Source'] = news_html.a.get_text().strip() + "--" + news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')
#    news_list.append(news)#append方法和list要放在同一级，不然会发生list元素重复！！            
#    for news in news_list:
#        for i in news.values():
#            print color.yellow(i)  

#for word in query_words: 
#    parameters = {'word': word}     
#    r = requests.get(news_base_url, params=parameters)#get到的新闻只有10条 
#    print r.text
#    soup = BeautifulSoup(r.text, 'lxml')
#    news_html_list = soup.select('div.result')#, limit = 5表示是5条新闻
#    for news_html in news_html_list:
#        news = {}
#        news_list = []
#        news['Title'] = news_html.a.get_text().strip() 
##        news['Title+Source'] = news_html.a.get_text().strip() + "--" + news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')
#        news_list.append(news)#append方法和list要放在同一级，不然会发生list元素重复！！            
#        for news in news_list:
#            for i in news.values():
#                print color.yellow(i)             

#def NewsMonitor():
#    query_words = Rows
#    news_base_url = 'http://news.baidu.com/ns?tn=news'
#    for word in query_words: 
#        parameters = {'word': word}        
#        r = requests.get(news_base_url, params=parameters)
#        soup = BeautifulSoup(r.text, 'lxml')
#        news_html_list = soup.select('div.result')#, limit = 5表示是5条新闻
##        news_list = []  #放在这里会造成新闻重复！！！      
#        for news_html in news_html_list:
#            news = {}
#            news_list = []
##            news['Title'] = news_html.a.get_text().strip() 
#            news['Title+Source'] = news_html.a.get_text().strip() + "--" + news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')
#            news_list.append(news)#append方法和list要放在同一级，不然会发生list元素重复！！            
#            for news in news_list:
#                for i in news.values():
#                    print color.yellow(i)
#    print "*"*50
#    t = Timer(15,NewsMonitor)
#    t.start()
#    
#if __name__ == "__main__": 
#    NewsMonitor()  
#中断ipython执行是Ctrl+D

'''
目标3：按新闻时间先后排序，但“2017年11月24日09:45”和“6小时前”不同格式的时间如何排？
'''


    
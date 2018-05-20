# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 19:33:29 2017

@author: zack zhang

和Ver3一样

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


query_word = '习近平'    
news_base_url = 'http://news.baidu.com/ns?tn=news'

news_url = news_base_url + query_word
parameters = {'word': query_word}

# 获取 JSON 数据
r = requests.get(news_base_url, params=parameters)
#print r.url

soup = BeautifulSoup(r.text, 'lxml')
news_html_list = soup.select('div.result')
news_list = []
#print news_html_list

for news_html in news_html_list:
    news = {}
    news['Title'] = news_html.a.get_text().strip()
    news['Source'] = news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')
#    news['Source'] = news_html.find('p', 'c-author').get_text().strip()
#    news['链接'] = news_html.a['href']
#    source = news_html.find('p', 'c-author').get_text().strip().replace('\xa0\xa0', ' ').split(' ')
#    news['来源'] = source[0]
#    news['发布日期'] = source[1]
    
    news_list.append(news)

def NewsMonitor():
    for news in news_list:
        for k, v in news.items():
            if k is 'Title':#不知道为什么用“标题”就出错用“Title”就没问题                
#                print color.red(k.decode('utf-8')), color.white_green(v)
                print color.white_green(v)
            else:
#                print k.decode('utf-8'), v
                print v 
    print "==$=="*10          
    t = Timer(15,NewsMonitor)
    t.start()
   
if __name__ == "__main__": 
  NewsMonitor()  



    
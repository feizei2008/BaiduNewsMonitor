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
    6、直接打印dic.vales而非dic的key、value,节省空间
    7、实现多关键词轮询
    8、搞清了百度新闻查询各参数的作用
    9、txt文件内容通过notepad++以utf-8无BOM编码格式保存
    10、urllib.urlencode将requests.get()所需的网站链接格式标准化
    11、每个关键词抓几条新闻可自由调整
    12、各关键词是抓“标题”or“标题+正文”可选取
存在问题：
   
尝试方案：
    1、用ghost.py（须pip安装Ghost.py非ghost.py）模拟用户浏览网页习惯，
       以解决js异步返回（疑似）、ajax等导致的抓取网页内容不完整问题，
       但模拟用户浏览网页比较耗资源。且最终模块使用失败。
    2、用urllib2抓取网页，失败
    3、用list的sorted方法对新闻按时间排序，
       但无法解决“2017年11月24日09:45”和“6小时前”不同格式的时间排序问题
    4、设定百度新闻搜索的bt参数来实现只搜索较新日期的新闻，但似乎不起作用

http://blog.csdn.net/semanwmj/article/details/7460274 百度新闻高级搜索URL中各个参数的意思
https://wenku.baidu.com/view/474d982a482fb4daa58d4b25.html 百度搜索url的参数说明与详细介绍
https://www.zhihu.com/question/20642243 如何追寻百度搜索结果url中的参数tn？

"""

import requests
import urllib
from bs4 import BeautifulSoup
from threading import Timer
import os
from datetime import datetime, timedelta
import arrow 

from colorama import  init, Fore, Back#, Style  
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

leaders = ['习近平', '李克强']

path = os.path.abspath(os.path.dirname(__file__))
File = path+'\query-words.txt'
Rows = open(File).read().splitlines()#为避免头部BOM问题，txt需用notepad++以utf-8无BOM编码格式保存         

#news_base_url = 'http://news.baidu.com/ns?tn=news'
#parameters = {'word': '习近平'}
#requests.get(news_base_url, params=parameters)
  
'''
pn=page number,搜索结果的页码，从零开始计数。即pn = ${结果页码-1}*rn
rn：Record Number，搜索结果显示条数，缺省设置rn=10，取值范围:10-100
cl：解释一（百度搜索）：Class，搜索类型，cl=3为网页搜索，cl=2为图片搜索(？存疑)
    解释二（百度新闻）：分别为1和2的时候，新闻的时间有差别，不明白是不是分别代表
                      “发表日期”和“被百度收录的日期”，建议用2(经张春雨验证，建议用1)
    解释三：cl=0为所有结果，即非相关页面有边角地方新闻标题带有搜索关键词的也会收录进来，不推荐
    个人理解：cl=0为所有结果，即非相关页面有边角地方新闻标题带有搜索关键词的也会收录进来，不推荐；
             cl=2为新闻标题包含关键词的，避免噪音干扰，相关性、权威性更强；
             cl=1为新闻标题+正文包含关键词的，极端要求时效性的可选此（如领导人动态）。
lm：搜索结果的时间限制。以天为单位，例如搜索最近一个月的网页，lm=30.默认值为0，表示没有时间限制
ct：语言限制。0-所有语言，1-简体中文网页，2-繁体中文网页；其它不确定或者无效。默认值为0
bt=0 开始日期的毫秒数，如2012-04-12 的毫秒数是1334160000
et=0 结束日期的毫秒数，注意是当天的23:59:59
rsv_bp: 搜索位置  0=首页，1=搜索结果顶部，2=搜索结果底部
bs: before search  上一次的搜索kw
sr: 结合bs使用。一般查询sr=0或者为空值，但sr=1时，查询将结合bs的值一起作为查询的关键字。
    默认值为0，除0，1外其它值无效。
f：搜索判断，f=8用户自主搜索，f=3下拉框推荐，f=1相关搜索；默认值为空
''' 

#query_words = Rows
#baseUrl = 'http://news.baidu.com/ns'
#for word in query_words:         
##    data = {'word': word, 'rn': '20','ct': '0', 'cl': '2', 'ie': 'utf-8',
##            'rsv_bp': '1', 'sr': '0', 'f': '8', 'prevct': 'no', 'tn': 'news'}#参数完全仿照网页
##    'ct'='0'不限语言,搜出的结果才全；
##    'ie': 'utf-8'加入会导致搜不出结果
#    cl = ['1' if word in leaders else '2'] 
#    print cl[0]*40
#    data = {'word': word, 'rn': '3','ct': '0', 'cl': cl[0]}
##   urlencode截取的参数为逗号前的数据，因此列表推导式'cl' : '1' if word in leaders else '1'无效
#    data = urllib.urlencode(data)
#    url = baseUrl + '?' + data
#    html = requests.get(url)
#    soup = BeautifulSoup(html.text, 'lxml')
#    news_html_list = soup.select('div.result')#, limit = 5表示是5条新闻
##        news_list = []  #放在这里会造成新闻重复！！！      
#    for news_html in news_html_list:
#        news = {}
#        news_list = []
##            news['Title'] = news_html.a.get_text().strip() 
#        news['Title+Source'] = news_html.a.get_text().strip() + "-" + news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')
#        news_list.append(news)#append方法和list要放在同一级，不然会发生list元素重复！！                 
#        for news in news_list:
#            for i in news.values():
#                print color.yellow(i)
        
#ThreeDaysAgo = datetime.now() - timedelta(2) 
#ThreeDaysAgoSec = arrow.get(ThreeDaysAgo).timestamp 秒表示的当前时间日期

def NewsMonitor():
    query_words = Rows
    baseUrl = 'http://news.baidu.com/ns'
    for word in query_words:
#       data = {'word': word, 'rn': '20','ct': '0', 'cl': '2', 'ie': 'utf-8',
#            'rsv_bp': '1', 'sr': '0', 'f': '8', 'prevct': 'no', 'tn': 'news'}#参数完全仿照网页
#       'ct'='0'不限语言,搜出的结果才全；
#       'ie': 'utf-8'加入会导致搜不出结果
        cl = ['1' if word in leaders else '2'] 
        print cl[0]*40
#        bt = str(ThreeDaysAgoSec) bt参数似乎并不起作用
        data = {'word': word, 'rn': '3','ct': '0', 'cl': cl[0]}
#       urlencode截取的参数为逗号前的数据，因此列表推导式'cl' : '1' if word in leaders else '1'无效
        data = urllib.urlencode(data)
        url = baseUrl + '?' + data
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        news_html_list = soup.select('div.result')#, limit = 5表示是5条新闻
#        news_list = []  #放在这里会造成新闻重复！！！      
        for news_html in news_html_list:
            news = {}
            news_list = []
#            news['Title'] = news_html.a.get_text().strip() 
            news['Title+Source'] = news_html.a.get_text().strip() + "-" + news_html.find('p', 'c-author').get_text().strip().replace(u'\xa0', u' ')
            news_list.append(news)#append方法和list要放在同一级，不然会发生list元素重复！！            
            for news in news_list:
                for i in news.values():
                    try:
                        print color.yellow(i)
                    except:
                        print color.yellow(i.encode('GBK', 'ignore'))
#关于gbk encode报错参见：https://www.crifan.com/unicodeencodeerror_gbk_codec_can_not_encode_character_in_position_illegal_multibyte_sequence/
    print color.magenta("*"*80)
    t = Timer(60,NewsMonitor)
    t.start()
    
if __name__ == "__main__": 
    NewsMonitor()  
#中断ipython执行是Ctrl+D

'''
目标3：按新闻时间先后排序，但“2017年11月24日09:45”和“6小时前”不同格式的时间如何排？
'''


    
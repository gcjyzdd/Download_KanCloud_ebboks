#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys# os list files and change file names
import time # sleep, count time
import platform
import random# generate random number and choose randomly
import re, json, cookielib
import urllib
import imghdr# check image type

#import threading
from datetime import datetime

#from lxml import html#xpath
from lxml import etree

from os import listdir
from os.path import isfile, join

# requirements
import requests, termcolor, html2text
try:
        from bs4 import BeautifulSoup
except:
        import BeautifulSoup

from selenium import webdriver


def get_IP_list():

	print 'Get IP proxy list'
	timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	ip_proxy='http://cn-proxy.com/'
	r=requests.get(ip_proxy)
	soup=BeautifulSoup(r.content,"lxml")

	thefile=open('IP_proxy_list.json','w')
	array=[];
	for item in soup.find_all('div',class_='table-container')[1].find('tbody').find_all('tr'):
		array.append(item.find('td').string)
	json.dump({'IP':array,'time':timestamp},thefile,indent=4)
	thefile.close()


class myWebdriver(webdriver):
    iplist=None
    ualist=None
    RUN=None
    def __init__(self):
	self.update_iplist()

    def myGet(self,url,timeout=40,proxy=None,num_retries=4,download_path):

	print u'webdriver开始打开 ',url

	self.update_iplist()

	if proxy==None:
	    try:
	        chromeOptions = webdriver.ChromeOptions()
		prefs = {"download.default_directory" : download_path}
		chromeOptions.add_experimental_option("prefs",prefs)
		#PROXY=random.choice(self.iplist)
		#chromeOptions.add_argument('--proxy-server=%s' % PROXY)

		chromedriver = "/usr/bin/chromedriver"
		driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=chromeOptions)
		driver.set_page_load_timeout(timeout)
		return driver.get(url)
	    except:
	        driver.quit()
	        if num_retries>0:
	    	    print u'webdriver打开网页失败，10s后重试，倒数第：%d次' % num_retries
		    time.sleep(10)
	            return self.get(url,timeout,None,num_retries-1)
	        else:
	            print u'webdriver开始使用代理'
		    time.sleep(10)

		    IP=random.choice(self.iplist)
		    proxy={'http':IP}
		    return self.get(url,timeout,proxy,)
	else:
	    print u'webdriver使用代理'
	    try:
		IP=random.choice(self.iplist)
		#print 'iplist type:', type(self.iplist)
		#print 'IP type:', IP
		proxy={'http':IP}
		print 'proxy:', proxy
		return requests.get(url,headers=headers,proxies=proxy,timeout=timeout)
	    except:
		if num_retries>0:
		    print u'webdriver正在使用代理，10s后重试，倒数第%d次' % num_retries
		    time.sleep(10)
		    print 'webdriver当前代理：%s' % proxy
		    return self.get(url,timeout,proxy,num_retries-1)

		else:
		    print u'webdriver使用代理获取失败，请检查网络连接。。。'
		    return self.get(url,3)

	def update_iplist(self):
	    now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	    with open('IP_proxy_list.json','r') as df:
	        data=json.load(df)
	        df.close()

	        bef=data['time']

	        start_dt = datetime.strptime(bef, '%Y-%m-%d %H:%M:%S')
	        end_dt = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
		diff = (end_dt - start_dt).seconds

		if diff>600:
		    get_IP_list()
		    with open('IP_proxy_list.json','r') as df:
			data=json.load(df)
			df.close()
			self.iplist=[];
			self.iplist=data['IP']
		else:
		    print 'IP proxy does not need to be updated'



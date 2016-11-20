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


def get_IP_list():


	print 'Get IP proxy list'
	timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	
	ip_proxy='http://cn-proxy.com/'
	r=requests.get(ip_proxy)
	soup=BeautifulSoup(r.content,"lxml")
	
	thefile=open('IP_proxy_list.json','w')
	array=[];
	for item in soup.find_all('div',class_='table-container')[1].find('tbody').find_all('tr'):
		array.append(item.find('td').string+':'+item.find_all('td')[1].string)
	json.dump({'IP':array,'time':timestamp},thefile,indent=4)
	thefile.close()


class Downloader:
	iplist=None
	ualist=None
	RUN=None
	def __init__(self):
		print 'Create a downloader'
		#ip_url="http://haoip.cc/tiqu.htm"
 		#r=requests.get(ip_url)
		#soup=BeautifulSoup(r.content,"lxml")
		#content=soup.find('div',class_="col-xs-12")
		
		#print 'get proxy'
		#self.iplist=[];
		#for i in re.findall(r"\s+(\d+.*)<",str(content)):
		#	self.iplist.append('http://'+i)
		
		self.RUN=True
		#threading.Thread(target=self.update_iplist(),name='Update IP proxy list').start()
		
		self.update_iplist()
		#print 'Hello!'
		self.ualist=["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
		 "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
		 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
		 "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
		 "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
		 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
		 "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
		 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
		 "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
		 "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		 "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
		 "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
		 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
		 "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]

	def get(self,url,timeout=10,proxy=None,num_retries=6):
		print u'开始获取',url
		UA=random.choice(self.ualist)
		headers={'User-Agent': UA}
		
		if proxy==None:
			try:
				return requests.get(url,headers=headers,timeout=timeout)
			except:
				if num_retries>0:
					print u'获取网页失败，10s后重试，倒数第：%d次' % num_retries					
					time.sleep(10)
					return self.get(url,timeout,None,num_retries-1)
				else:
					print u'开始使用代理'
					time.sleep(10)
					
					IP=random.choice(self.iplist)
					proxy={'http':IP}
					return self.get(url,timeout,proxy,)
		else:
			print u'使用代理'
			try:				
				IP=random.choice(self.iplist)
				#print 'iplist type:', type(self.iplist)
				#print 'IP type:', IP
				proxy={'http':IP}
				print 'proxy:', proxy
				return requests.get(url,headers=headers,proxies=proxy,timeout=timeout)
			except:
				if num_retries>0:
					print u'正在使用代理，10s后重试，倒数第%d次' % num_retries
					time.sleep(10)
					print '当前代理：%s' % proxy								
					return self.get(url,timeout,proxy,num_retries-1)
					
				else:
					print u'使用代理获取失败，请检查网络连接。。。'
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

	

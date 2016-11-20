#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys# os list files and change file names
import time # sleep, count time
import platform
import random# generate random number and choose randomly
import re, json, cookielib
import urllib


import json
import urllib2
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


from Downloader import Downloader

from selenium import webdriver
from multiprocessing import Pool,Queue# apply pool to utilize multiprocess
import subprocess# run bash

import itertools

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

url_start='http://www.kancloud.cn/explore/top'
host='http://www.kancloud.cn'

BOOKS=range(833)

class book():
    def __init__(self,ID,link,name,abstract,cover,formats,tags,img_link=None,dlable=False):
        self.ID='%06d'%ID
        self.link=link
        self.name=name
        self.abstract=abstract
        self.cover=cover
        self.formats=formats
        self.tags=tags
        self.cover_link=img_link
        self.downloadable=dlable

    def dump(self):
    	return {'ID':self.ID,
    	        'link':self.link,
    	        'name':self.name,
    	        'abstract':self.abstract,
                'cover':self.cover,
    	        'formats':self.formats,
    	        'tags':self.tags,
                'cover_link':self.cover_link,
                'downloadable':self.downloadable}

class BookChecker():
	def __init__(self):
	    self.dl=Downloader()


        def get_max_page(self):
            soup=self.soup
            list_a=soup.find('div',class_='m-paging').find_all('a')
            self.max_page=int(soup.find('div',class_='m-paging').find('a',class_='end').string)
            print 'max page = ',self.max_page

        def get_url_list(self,url):
	    r=self.dl.get(url)
	    soup=BeautifulSoup(r.content,"lxml")
            list_items=soup.find('div',class_='m-manual-list manual-list-recome').find_all('div',class_='list-item')
            url_list=[]
            for item in list_items:
                url_list.append(item.dl.dd.a['href'])
            return host+url_list

        def get_all_urls(self):
            LIST=[]
            for i in range(self.max_page):
                url='http://www.kancloud.cn/explore/top?page='+str(i)
                LIST+=self.get_url_list(url)

def multi_run_wrapper(args):
    return get_book_info(*args)

def get_book_info(url,ind):
    print 'HELLO ...'
    dl=Downloader()
    r=dl.get(url)
    print 'HELLO2'
    soup=BeautifulSoup(r.content,"lxml")
    desp=soup.find('p',{'id':'articleDescription'}).text
    print 'description:\n',desp.encode('utf-8')
    title=soup.find('h1',id='articleTitle').text
    #print 'title\n',title

    dlable=False
    try:
        aa=soup.find('div',id='manualDownload').find('span').find('b').find('i')
        if aa:
            dlable=True
        else:
            dlable=False
    except:
        pass

    #print 'Downloadable: ',dlable
    tags=[]
    try:
        bb=soup.find('p',class_='label-box').find_all('span')
        #print 'bb',bb
        tags=[i.text.strip() for i in bb]
    except:
        pass
    #print 'tags:',tags
    formats=[]
    try:
        aa=soup.find('div',id='manualDownload').find('div',class_='drop-hide').find('div').find('ul').find_all('li')
        for item in aa:
            #print item.text.encode('utf-8')
            formats.append(re.findall(r'\s(.*)',item.text.strip())[0])
    except:
        pass
    #print 'Formats:',formats
    img_link=''
    try:
        img_link=soup.find('a',class_='e-cover').img['src']
    except:
        pass
    print img_link

    print 'get book'
    return book(ind,url,title,desp,'./cover',formats,tags,img_link,dlable)

#    def __init__(self,ID,link,name,abstract,cover,formats,tags,img_link=None,dlable=False):


def main():
    #a=BookChecker()
    #LIST_URL=a.get_all_urls()

    LIST_URL=[]
    thefile=open('LIST_URL.txt','r')
    for item in thefile:
        LIST_URL.append(host+item[0:-1])
    thefile.close()
    LEN=len(LIST_URL)
    print 'length = ',LEN
    NTH=8
    p=Pool(NTH)
    ind=0

    ARGS=[]
    for i in range(LEN):
        ARGS.append((LIST_URL[i],i))

    Books=p.map(multi_run_wrapper,ARGS)

#    for url in LIST_URL[0:15]:
#        #print host+url
#        Books.append(p.apply_async(get_book_info,args=(url,ind,)))
#        ind+=1
#        time.sleep(10e-6)
#    print '%d tasks' % ind
#    print 'wait for pool ...'
#    p.close()
#    p.join()
    print 'pool finished.'

    return Books

if __name__=='__main__':
    #testq=Queue()
    get_book_info("http://www.kancloud.cn/digest/iaccepted",2)
    Books=main()


    json_string=[o.dump() for o in Books]
    thefile=open('BOOK_LIST.json','w')
    json.dump({'Books_info':json_string,'Total':833},thefile,indent=4)
    thefile.close()

    sys.exit('EXIT.')

#get_book_info("http://www.kancloud.cn/digest/iaccepted")
#get_book_info("http://www.kancloud.cn/wizardforcel/the-boost-cpp-libraries")
#get_book_info("http://www.kancloud.cn/wangshubo1989/new-characteristics")
#
#book1=book(1,'http://1','hekko book','example book','./a.jpeg',['pdf','epub','mobi'],['Web','C++'])
#book2=book(2,'http://2','hekko book2','example book2','./a.jpeg',['pdf','epub'],['Web','C++','Python'])
#book3=book(3,'http://3','hekko book3','example book3','./a.jpeg',['mobi'],['Web','C++','Big Data'])
#
#books=[book1,book2,book3]
#json_string=[o.dump() for o in books]
#
##print json_string
#
#thefile=open('testexp1.json','w')
#json.dump({'Books_info':json_string,'Total':3},thefile,indent=4)
#thefile.close()
#
#df=open('testexp1.json','r')
#data=json.load(df)
#df.close()
#
#print data['Total']
#print data['Books_info'][0]['ID']
#

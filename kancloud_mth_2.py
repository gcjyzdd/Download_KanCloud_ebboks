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
from multiprocessing import Pool# apply pool to utilize multiprocess
import subprocess# run bash


# set chromedriver path and download path
chromeOptions = webdriver.ChromeOptions()
dl_path="/home/changjie/Downloads/KanCloud4"
prefs = {"download.default_directory" : dl_path}
chromeOptions.add_experimental_option("prefs",prefs)
PROXY='1.82.216.134:80'
#chromeOptions.add_argument('--proxy-server=%s' % PROXY)

chromedriver = "/usr/bin/chromedriver"
#driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=chromeOptions)
#driver.set_page_load_timeout(40)

url_start='http://www.kancloud.cn/explore/top'
host='http://www.kancloud.cn'

class Download_Kan_Cloud():
	def __init__(self):
		self.dl=Downloader()
		r=self.dl.get(url_start)
		self.soup=BeautifulSoup(r.content,"lxml")

        def get_max_page(self):
            soup=self.soup
            list_a=soup.find('div',class_='m-paging').find_all('a')
            self.max_page=int(soup.find('div',class_='m-paging').find('a',class_='end').string)
            print 'max page = ',self.max_page

        def get_page_hrefs(self,url):
	    r=self.dl.get(url)
	    soup=BeautifulSoup(r.content,"lxml")
            list_items=soup.find('div',class_='m-manual-list manual-list-recome').find_all('div',class_='list-item')
            url_list=[]
            for item in list_items:
                url_list.append(item.dl.dd.a['href'])
            return url_list

        def download_url(self,url):
#           open the url
	    driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=chromeOptions)
	    driver.set_page_load_timeout(120)
            try:
                driver.get(url)
            except:
                NUM_TRY=5
                for ii in range(NUM_TRY):
                    driver.quit()
                    print 'webdriver open url failed.'
                    print 'webdriver uses PROXY now.'
	            self.dl.update_iplist()
                    PROXY=random.choice(self.dl.iplist)
                    print 'PROXY: '
                    print PROXY

                    chromeOptions.add_argument('--proxy-server=%s' % PROXY)
                    driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=chromeOptions)
	            driver.set_page_load_timeout(300)
                    try:
                        driver.get(url)
                        break
                    except:
                        print 'webdriver open url failed.', str(ii)
                        if ii==NUM_TRY-1:
                            sys.exit('EXIT!!!!!!')
            #check if this book is downloadable
            try:
                driver.find_element_by_xpath('//*[@id="manualDownload"]/span/b').click()
                print 'Download: ', url
                print driver.find_element_by_xpath('//*[@id="articleTitle"]').text
                for i in range(1,4):
                    try:
                        dlinks=driver.find_element_by_xpath('//*[@id="manualDownload"]/div/div/ul/li['+str(i)+']/a').click()
                        driver.find_element_by_xpath('//*[@id="manualDownload"]/span/b').click()
                        time.sleep(5)
                    except:
                        pass
                while( not check_download(dl_path)):
                    time.sleep(5)
                driver.quit()
            except:
                print driver.find_element_by_xpath('//*[@id="articleTitle"]').text
                print 'This book cannot be downloaded.'
            	driver.quit()


def check_download(path):
    aa = subprocess.check_output(["/bin/bash","-c","ls  "+path]).decode('utf-8').strip()
    if re.search(r'.*(\.crdownload).*',aa):
        print 'Downloading...'
        return False
    else:
        print 'Download finished.'
        return True

def download_book(url):
    print 'url = ',url
    d=Download_Kan_Cloud()
    d.download_url(url)


def main():
    kl=Download_Kan_Cloud()
    kl.get_max_page()

    LIST_URL=[]
    for i in range(1,1+kl.max_page):#1+kl.max_page
        print ['PAGE %d' % i][0].center(80,'*')
        list_url=kl.get_page_hrefs('http://www.kancloud.cn/explore/top?page='+str(i))
        LIST_URL+=list_url

    print 'Get %d book urls' % len(LIST_URL)

    thefile=open('LIST_URL.txt','w')
    for item in LIST_URL:
        thefile.write("%s\n" % item)
    thefile.close()

    NTH=6
    BATCH=NTH*10
    LEN=len(LIST_URL)

    ind=0
    flag=1

    print 'Use webdriver to download books ...'
    while(flag):
        print 'Download %d of %d,batch=%d' %(ind,LEN,BATCH)
        p=Pool(NTH)
        for i in range(BATCH):
            if ind==LEN-1:
                flag=0
                p.apply_async(download_book,args=(host+LIST_URL[ind],))
                break
            else:
                p.apply_async(download_book,args=(host+LIST_URL[ind],))
                ind+=1
        print 'ind=%d' % ind
        print 'wait for pool ...'
        p.close()
        p.join()
        print 'pool finished.'

    print 'All are downloaded. EXIT.'

if __name__=='__main__':
    main()


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

from kan_db import get_downloadable_links


# set chromedriver path and download path
chromeOptions = webdriver.ChromeOptions()
dl_path="/home/changjie/Downloads/KanCloud2"
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
        #open the url
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
            for i in range(0,4):
                try:
                    dlinks=driver.find_element_by_xpath('//*[@id="manualDownload"]/div/div/ul/li['+str(i)+']/a').click()
                    driver.find_element_by_xpath('//*[@id="manualDownload"]/span/b').click()
                    time.sleep(5)
                except:
                    pass
            timer=0
            while( not check_download(dl_path) and timer<600):
                time.sleep(5)
                timer+=5
            driver.quit()
            if timer <600:
                print 'Download finished:',driver.find_element_by_xpath('//*[@id="articleTitle"]').text
            else:
                print 'Download takes too long, drop it: ',driver.find_element_by_xpath('//*[@id="articleTitle"]').text

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

def download_book(url,ind):
    print '%d link :%s = ' %(ind,url)
    d=Download_Kan_Cloud()
    d.download_url(url)


def main():

    LIST_URL=get_downloadable_links();
    print 'list[0]=',LIST_URL[0]
    print 'Get the url list.'
    try:
        print 'AA : ',LIST_URL[0][0]
        request.get(LIST_URL[0].decode('utf-8'))
        print 'successed!'
    except:
        print 'url wrong'
    #sys.exit('EXIT')

    NTH=8
    ind=0

    print 'Use webdriver to download books ...'

    p=Pool(NTH)
    for url in LIST_URL:
        ind+=1
        print ['Download %d of %d links' % (ind,len(LIST_URL)) ][0][0].center(60,'*')
        p.apply_async(download_book,args=(url[0],ind,))

    print 'wait for pool ...'
    p.close()
    p.join()
    print 'pool finished.'

    print 'All are downloaded. EXIT.'

if __name__=='__main__':
    main()


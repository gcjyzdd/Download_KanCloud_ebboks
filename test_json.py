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



class book():
    def __init__(self,ID,link,name,abstract,cover,formats,tags):
        self.ID='%06d'%ID
        self.link=link
        self.name=name
        self.abstract=abstract
        self.cover=cover
        self.formats=formats
        self.tags=tags

    def dump(self):
    	return {'ID':self.ID,
    	        'link':self.link,
    	        'name':self.name,
    	        'abstract':self.abstract,
                'cover':self.cover,
    	        'formats':self.formats,
    	        'tags':self.tags}

book1=book(1,'http://1','hekko book','example book','./a.jpeg',['pdf','epub','mobi'],['Web','C++'])
book2=book(2,'http://2','hekko book2','example book2','./a.jpeg',['pdf','epub'],['Web','C++','Python'])
book3=book(3,'http://3','hekko book3','example book3','./a.jpeg',['mobi'],['Web','C++','Big Data'])

books=[book1,book2,book3]
json_string=[o.dump() for o in books]

print json_string

thefile=open('testexp1.json','w')
json.dump({'Books_info':json_string,'Total':3},thefile,indent=4)
thefile.close()

df=open('testexp1.json','r')
data=json.load(df)
df.close()

print data['Total']
print data['Books_info'][0]['ID']


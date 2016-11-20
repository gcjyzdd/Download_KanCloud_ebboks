#!/usr/bin/python
# -*- coding: utf-8 -*-


from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "/home/changjie/Downloads/KanCloud"}
chromeOptions.add_experimental_option("prefs",prefs)


driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get('http://www.kancloud.cn/digest/ios-mac-study')

#print driver.find_element_by_link_text(u'下载 PDF')
#manualDownload > div > div > ul > li:nth-child(2) > a

driver.find_element_by_xpath('//*[@id="manualDownload"]/span/b').click()
dlink=driver.find_element_by_xpath('//*[@id="manualDownload"]/div/div/ul/li[2]/a')
print dlink
aa=dlink.click()
print type(aa)


# body > div.m-wrap > div > div.page-body > div.container > div.m-tab.tab-theme-b > div.tab-wrap > div > div > div:nth-child(1) > dl > dt > a > img
# body > div.m-wrap > div > div.page-body > div.container > div.m-tab.tab-theme-b > div.tab-wrap > div > div
# //*[@id="manualDownload"]/div/div/ul/li[2]/a
# //*[@id="manualDownload"]/div/div/ul/li[3]/a



# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:18:44 2016

@author: manish
"""

import urllib2
from xml.etree import ElementTree as etree

# RSS Feeds from BBC BUSINESS
#############################
def BBCBusiness():
    feed = urllib2.urlopen('http://feeds.bbci.co.uk/news/business/rss.xml')
    return parseRSS(feed)

# RSS Feeds from WALL STREET JOURNAL
####################################
def WSJMarkets():
    feed = urllib2.urlopen('http://www.wsj.com/xml/rss/3_7031.xml')
    return parseRSS(feed)

def WSJUSBusiness():
    feed = urllib2.urlopen('http://www.wsj.com/xml/rss/3_7014.xml')
    return parseRSS(feed)          

# RSS Feeds from THOMPSON REUTERS
################################# 
def ReutersBusiness():
    feed = urllib2.urlopen('http://feeds.reuters.com/reuters/businessNews')
    return parseRSS(feed)
    
def ReutersCompany():
    feed = urllib2.urlopen('http://feeds.reuters.com/reuters/companyNews')
    return parseRSS(feed)

def ReutersHotStock():
    feed = urllib2.urlopen('http://feeds.reuters.com/reuters/hotStocksNews')
    return parseRSS(feed)

# RSS Feeds from CNN
####################
def CNNBusiness():
    feed = urllib2.urlopen('http://rss.cnn.com/rss/money_news_international.rss')
    return parseRSS(feed)

# RSS Feed Parser
#################
def parseRSS(feed):
    feed_data = feed.read()
    feed.close()
    
    feed_root = etree.fromstring(feed_data)
    item = feed_root.findall('channel/item')
    feeds = []

    for entry in item:
        item = {}
        item['link'] = entry.findtext('link')
        item['date'] = entry.findtext('pubDate')
        feeds.append(item)
        
    return feeds
    

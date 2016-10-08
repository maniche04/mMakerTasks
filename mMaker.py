"""1
Created on Wed Oct 05 15:36:08 2016

@author: manish
"""
from time import strftime
import pytz
import dateutil
from newspaper import Article
import MarketFeeds
from DBConnection import getConnection
local_tz = pytz.timezone('Asia/Dubai')

conn = getConnection()
c = conn.cursor()

def fetchBBC():
    fetchArticles(MarketFeeds.BBCBusiness(),'1','BBC Business')

def fetchReuters():
    fetchArticles(MarketFeeds.ReutersBusiness(),'2','Reuters Business')
    fetchArticles(MarketFeeds.ReutersCompany(),'2','Reuters Company')
    fetchArticles(MarketFeeds.ReutersHotStock(),'2','Reuters Hot Stock')
    
## Reads the News from the Sources
##################################
def fetchArticles(feeds,source,name):
    print("Fetching articles from " + name)
    total = 0
    for feed in feeds:
        news = Article(feed['link'])
        news.download()
        news.parse()
        feed['source'] = source
        feed['title'] = news.title.encode('utf-8')
        feed['text'] = news.text.encode('utf-8')
        feed['article_html'] = news.article_html
        feed['image'] = news.top_image
        c.execute('SELECT COUNT(*) as count FROM news_articles WHERE link = %s',(feed['link'],))
        result = c.fetchone()
        if (result['count'] < 1):
            date = dateutil.parser.parse(feed['date'])
            #print(feed['title'] + ' | ' + feed['link'])
            c.execute('INSERT INTO news_articles (sourceId,title,link,pubDate,image,articlehtml, body,evalFlag,score,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(feed['source'],feed['title'],feed['link'],date,feed['image'],feed['article_html'], feed['text'],0,0,strftime("%Y-%m-%d %H:%M:%S"),strftime("%Y-%m-%d %H:%M:%S")))
            total = total + 1
    print(str(total) + ' new news from ' + name)  


fetchBBC()
fetchReuters()

conn.commit()
conn.close()
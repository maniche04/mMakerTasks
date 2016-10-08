# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 16:49:37 2016

@author: manish
"""
import pandas as pd
from DBConnection import getConnection
conn = getConnection()
c = conn.cursor()

def readJson(filename):
    df = pd.read_json(filename)
    df = df.drop('title',1)
    return df
    
def cleanText(text):
    text = text.lower()
    
    from bs4 import BeautifulSoup
    text = BeautifulSoup(text).get_text()
    
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    
    from nltk.corpus import stopwords
    clean = [word for word in text if word not in stopwords.words('english')]
    return clean
    
def loadPositive():
    myfile = open('positives.csv',"r")
    positives = myfile.readlines()
    positive = [pos.strip().lower() for pos in positives]
    return positive
    
def loadNegative():
    myfile = open('negatives.csv',"r")
    negatives = myfile.readlines()
    negative = [neg.strip().lower() for neg in negatives]
    return negative

def countPos(cleantext, positive):
    pos = [word for word in cleantext if word in positive]
    return len(pos)
    
def countNeg(cleantext,negative):
    negs = [word for word in cleantext if word in negative]
    return len(negs)
    
def getSentiment(cleantext,negative,positive):
    return (countPos(cleantext,positive) - countNeg(cleantext, negative))

def calculateSentiment(df):
    positive = loadPositive()
    negative = loadNegative()
    df['cleantext'] = df['text'].apply(cleanText)
    df['score'] = df['cleantext'].apply(lambda x: getSentiment(x,negative,positive))
    return df
    
def evalSentiment(title,link,text):
    positive = loadPositive()
    negative = loadNegative()
    score = getSentiment(cleanText(text),negative,positive)
    c.execute("UPDATE news_articles SET score = %s, evalflag = 1 WHERE link = %s",(score,link))
    print(str(title.encode('utf-8')) + " | SCORE => " + str(score))
    
data = pd.read_sql_query("SELECT * FROM news_articles WHERE evalflag = 0",conn)

for i in range(0,len(data)):
    evalSentiment(data.iloc[i]['title'].decode('UTF-8'),data.iloc[i]['link'],data.iloc[i]['body'])
    
conn.commit()
conn.close()
    









    
    
    
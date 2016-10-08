# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 17:53:34 2016

@author: manish
"""

#import sqlite3

#conn = sqlite3.connect('mmaker.db')
#c = conn.cursor()
#
#for row in c.execute('SELECT title,score FROM news ORDER BY SCORE ASC'):
#       print row

#c.execute('DROP TABLE news')
#conn.commit()
#conn.close()

import pymysql.cursors

def getConnection():
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='mmaker',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

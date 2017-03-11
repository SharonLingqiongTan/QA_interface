#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, sys, datetime
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path

def getNumOfTagged(form, environ):
    result = cookieAuthentication(environ)
    if not result: return

    topic_id = int(form.getvalue("topic_id", None))
    atn_db  = DBHandler(db_path.atn)

    atn_db.cur.execute('''
        SELECT COUNT(1) FROM search_list, filter_list 
        WHERE search_list.topic_id = filter_list.topic_id
        AND search_list.docno = filter_list.docno
        AND search_list.topic_id = ?
        AND filter_list.state = 1
    ''', [int(topic_id)])  
    tagged_count, = atn_db.cur.fetchone()

    atn_db.close()

    print('Content-Type: text/plain\r\n')
    print(str(tagged_count))

# __main__

form = cgi.FieldStorage()
getNumOfTagged(form, environ)

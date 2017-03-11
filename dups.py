#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler

def dupsummary():
    atn_db = DBHandler("./database/test.db")
    fh = open('./view/nonrelevant.csv','w')
    atn_db.cur.execute('''
        SELECT filter_list.topic_id, filter_list.docno FROM filter_list, topic 
        WHERE filter_list.topic_id=topic.topic_id
        AND topic.state!=2 
        AND topic.userid<=6
        AND filter_list.state=2
        ORDER BY filter_list.topic_id
        ''')
    dups = atn_db.cur.fetchall()
    for dup in dups:
        fh.write(str(dup[0])+','+dup[1]+'\n')
    fh.close()
dupsummary()


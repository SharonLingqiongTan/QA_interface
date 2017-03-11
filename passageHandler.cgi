#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, datetime, sys
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog
import postNugget

def passageHandle(form, environ):

    result = cookieAuthentication(environ)
    if result:
        ## subtopic-user matching check
        userid, username, usercookie = result

        docno        = form.getvalue("docno", 0)
        offset_start = form.getvalue("offset_start", 0)
        offset_end   = form.getvalue("offset_end", 0)
        passage_name = form.getvalue("passage_name", None)
        subtopic_id  = form.getvalue("subtopic_id", None)

        atn_db  = DBHandler(db_path.atn)

        atn_db.insert('passage',[None,passage_name.decode('UTF-8'),docno,offset_start,offset_end,0,int(subtopic_id),0])
        passage_id = atn_db.cur.lastrowid #get the row id as the passage id

        atn_db.cur.execute('SELECT topic_id, subtopic_name FROM subtopic WHERE subtopic_id=?',[int(subtopic_id)])
        topic_id, subtopic_name = atn_db.cur.fetchone()
        atn_db.cur.execute('SELECT userid, topic_name, domain_id FROM topic WHERE topic_id=?',[topic_id])
        userid, topic_name, domain_id = atn_db.cur.fetchone()
        atn_db.cur.execute('SELECT username FROM user WHERE userid=?',[userid])
        username, = atn_db.cur.fetchone()

        corpus = ['EBOLA', 'POLAR', 'WEAPON'][domain_id-1]

        m1 = m2 = ''
        try: 
            m1, m2 = postNugget.postNugget(userid, topic_id, int(subtopic_id), corpus, passage_id, docno, passage_name)
        except: 
            pass

        atn_db.cur.execute('SELECT * FROM filter_list WHERE topic_id=? AND docno=?', [topic_id, docno])

        exist_check = atn_db.cur.fetchone()

        if not exist_check:
            atn_db.insert('filter_list', [topic_id, docno, 1])

        try:
            mylog.log_add_passage(username, topic_id, topic_name, subtopic_id, subtopic_name, passage_id, passage_name, docno)
        except:
            pass

        atn_db.commit()
            
        print('Content-Type: text/plain\r\n')
        print(passage_id)

    atn_db.close()

# __main__

form = cgi.FieldStorage()
passageHandle(form, environ)

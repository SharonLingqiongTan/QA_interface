#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, sys, datetime
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog
import postNugget


def gradeHandle(form, environ):
    result = cookieAuthentication(environ)
    if not result: return

    userid, username, usercookie = result

    score = form.getvalue("score", None)
    passage_id = form.getvalue("passage_id", None)
    topic_id = int(form.getvalue("topic_id", None))
    
    atn_db  = DBHandler(db_path.atn)

    atn_db.cur.execute('UPDATE passage SET grade=? WHERE passage_id=?',[int(score), int(passage_id)])
    
    atn_db.cur.execute('SELECT userid, domain_id FROM topic WHERE topic_id=?',[topic_id])
    userid, domain_id= atn_db.cur.fetchone()
    atn_db.cur.execute('SELECT username FROM user WHERE userid=?',[userid])
    username, = atn_db.cur.fetchone()
    atn_db.cur.execute('SELECT subtopic_id FROM passage WHERE passage_id=?',[int(passage_id)])
    subtopic_id, = atn_db.cur.fetchone()

    corpus = ['EBOLA', 'POLAR', 'WEAPON'][domain_id-1]
    m1 = m2 = ''
    try: 
        m1, m2 = postNugget.gradeNugget(userid, topic_id, subtopic_id, corpus, int(passage_id), score)
    except:
        pass
        
    
    try: mylog.log_grade_passage(username, passage_id, score)
    except: pass

    print("Status: 200 OK\r\n")

    atn_db.commit()

    atn_db.close()

# __main__

form = cgi.FieldStorage()
gradeHandle(form, environ)

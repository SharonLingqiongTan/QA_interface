#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, sys, datetime
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog

def putbackHandle(form, environ):
    result = cookieAuthentication(environ)
    if not result: return

    userid, username, usercookie = result

    topic_id = form.getvalue("topic_id", None)
    docno = form.getvalue("docid", None)
    atn_db  = DBHandler(db_path.atn)
    atn_db.cur.execute("SELECT state FROM filter_list WHERE topic_id=? AND docno=?", [int(topic_id), docno])
    ostate, = atn_db.cur.fetchone()
    if ostate == 2: origin = 'irrelevant'
    else: origin = 'duplicate'
    atn_db.cur.execute("DELETE FROM filter_list WHERE topic_id=? AND docno=?", [int(topic_id), docno])
    atn_db.commit()

    try: mylog.log_putback(username, origin, topic_id, docno)
    except: pass
    atn_db.close()

    print("Status: 200 OK\r\n")

# __main__

form = cgi.FieldStorage()
putbackHandle(form, environ)
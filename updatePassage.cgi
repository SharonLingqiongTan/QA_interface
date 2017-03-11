#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, datetime
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog

def updatePassage(form, environ):
    result = cookieAuthentication(environ)
    if not result: return

    userid, username, usercookie = result

    passage_id = form.getvalue("passage_id")
    subtopic_id = form.getvalue("subtopic_id") 
    topic_id = form.getvalue("topic_id")

    atn_db  = DBHandler(db_path.atn)

    atn_db.cur.execute('UPDATE passage SET subtopic_id=? WHERE passage_id=?',[int(subtopic_id), int(passage_id)])

    try: mylog.log_replace_passage(username, passage_id, subtopic_id)
    except: pass    

    atn_db.commit()
    atn_db.close()
    print("Status: 200 OK\r\n")

# __main__

form = cgi.FieldStorage()
updatePassage(form, environ)

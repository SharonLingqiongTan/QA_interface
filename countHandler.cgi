#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path

def countHandle(form, environ):
    result = cookieAuthentication(environ)
    if not result: return

    topic_id = form.getvalue("topic_id", None)
    atn_db  = DBHandler(db_path.atn)
    atn_db.cur.execute("SELECT COUNT (1) FROM filter_list WHERE topic_id=?", [int(topic_id)])
    count, = atn_db.cur.fetchone()
    atn_db.commit()
    atn_db.close()

    print("Content-Type: text/plain\r\n")
    print(str(count))

# __main__

form = cgi.FieldStorage()
countHandle(form, environ)
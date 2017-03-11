#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog

def logstateHandle(form, environ):
    result = cookieAuthentication(environ)
    if result:

        tmp, username, usercookie = result

        userid = form.getvalue("userid", None)
        loption = form.getvalue("l", None)
        topic_id = form.getvalue("topic_id", None)

        atn_db  = DBHandler(db_path.atn)

        ## topic-user matching check
        atn_db.cur.execute('UPDATE user SET loption=? WHERE userid=?', [int(loption), int(userid)])
        atn_db.commit()

        atn_db.cur.execute('SELECT topic_name FROM topic where topic_id=?', [int(topic_id)])
        topic_name, = atn_db.cur.fetchone()

        if loption == '0': text = 'show'
        else: text = 'hide'

        try: mylog.log_show_hide_tagged(username, text, topic_id, topic_name)
        except: pass

        print("Status: 200 OK\r\n")

    atn_db.close()

form = cgi.FieldStorage()
logstateHandle(form, environ)

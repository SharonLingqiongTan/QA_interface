#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path

def logstateHandle(form, environ):
    result = cookieAuthentication(environ)
    if result:

        docno = form.getvalue("docno", None)
        topic_id = form.getvalue("topic_id", None)

        atn_db  = DBHandler(db_path.atn)

        ## topic-user matching check
        atn_db.cur.execute('UPDATE topic SET level=?, docno=? WHERE topic_id=?', ['D', docno, int(topic_id)])
        atn_db.commit()

        atn_db.cur.execute('SELECT state FROM filter_list WHERE topic_id=? AND docno=?', [int(topic_id), docno])
        tmpresult = atn_db.cur.fetchone()
        if tmpresult:
            state, = tmpresult
        else:
            state = 0
        print('Content-Type: text/html\r\n')
        print(str(state))

    atn_db.close()

form = cgi.FieldStorage()
logstateHandle(form, environ)

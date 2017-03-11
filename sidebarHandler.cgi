#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, json
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path

def sidebarHandle(form, environ):
    topic_id = form.getvalue('topic_id',None)

    atn_db  = DBHandler(db_path.atn)

    result = cookieAuthentication(environ)
    if result:
        ## topic-user matching check
        sidebar = []
        atn_db.cur.execute('SELECT subtopic_id, subtopic_name FROM subtopic WHERE topic_id=? AND state=0',[int(topic_id),])
        subtopics = atn_db.cur.fetchall()
        for subtopic in subtopics:
            subdata = list(subtopic)
            atn_db.cur.execute('SELECT passage_id, passage_name, docno, grade FROM passage WHERE subtopic_id=? AND state < 2',[subdata[0]])
            passages = atn_db.cur.fetchall()
            for passage in passages:
                appendpassage = list(passage)
                appendpassage[1] = appendpassage[1].encode('UTF-8')
                subdata.append(appendpassage)
            sidebar.append(subdata)
        print('Content-Type: application/json\r\n')
        print(json.dumps(sidebar))
        ## json.dump encoder.encode??
    atn_db.close()

# __main__

form = cgi.FieldStorage()
sidebarHandle(form, environ)



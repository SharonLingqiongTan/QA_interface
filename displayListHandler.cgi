#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, datetime
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog

def displayListHandle(form, environ):
    result = cookieAuthentication(environ)
    if result:

        domain_id = form.getvalue("domain_id", None)
        topic_id = form.getvalue("topic_id" , None)
        type = form.getvalue("type" , None)
        username = form.getvalue("username", None)

        atn_db = DBHandler(db_path.atn)

        if type == "tagged":
            atn_db.cur.execute('SELECT docno FROM filter_list WHERE topic_id=? AND state=1', [int(topic_id)])
            title = "Tagged"
        elif type == "discarded":
            type = "irrelevant"
            atn_db.cur.execute('SELECT docno FROM filter_list WHERE topic_id=? AND state=2', [int(topic_id)])
            title = "Irrelevant"
        elif type == "duplicate":
            atn_db.cur.execute('SELECT docno FROM filter_list WHERE topic_id=? AND state=3', [int(topic_id)])
            title = "Duplicate"

        try: mylog.log_view_tagged_discarded_doc(username, title.lower(), topic_id)
        except: pass

        results = atn_db.cur.fetchall()
        atn_db.cur.execute('SELECT topic_name FROM topic WHERE topic_id=?',[int(topic_id)])
        topic_name, = atn_db.cur.fetchone()
        
        html = open("./html/displayList.html",'r')
        string = ""
        number = len(results)
        for docno, in results:
            if type == "tagged":
                   string += "<div><li>%s</li></div>"%docno
            else:
                string += "<div><li>%s</li> <span class='trash' data='%s'>put it back</span></div>"%(docno,docno)

        atn_db.cur.execute('SELECT domain_url FROM domain WHERE domain_id=?', [int(domain_id)])
        domain_url, = atn_db.cur.fetchone()
        print("Content-Type: text/html\r\n")
        print(html.read()%("'" + domain_url + "'", topic_id, title, topic_name, title.lower(), str(number), string))
        html.close()
        atn_db.close()

form = cgi.FieldStorage()
displayListHandle(form, environ)

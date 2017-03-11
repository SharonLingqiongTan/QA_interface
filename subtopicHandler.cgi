#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, datetime
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog

def subtopic_nameCheck(subtopic_name, subtopic_id, topic_id, atn_db):
    atn_db.cur.execute('SELECT subtopic_name FROM subtopic WHERE topic_id=? AND state=0 AND subtopic_id!=?',[int(topic_id),int(subtopic_id)])
    names = atn_db.cur.fetchall()
    for name, in names:
	if name.lower() == subtopic_name.lower():
	    return True
    return False
    
def subtopicHandle(form, environ):
    result = cookieAuthentication(environ)
    if result:
        userid = form.getvalue("userid", None)
        topic_id = form.getvalue("topic_id", '0')
        subtopic_id = form.getvalue("subtopic_id", '0')
        subtopic_name = form.getvalue("subtopic_name", "")
        subtopic_name = ' '.join(subtopic_name.split())
        
        atn_db  = DBHandler(db_path.atn)
    
        ## for add: topic-user matching check
        ## for edit: subtopic-user matching check
        flag = subtopic_nameCheck(subtopic_name, subtopic_id, topic_id, atn_db)
        if flag:
            response = 0
        else:
            if subtopic_id != '0':
                # edit subtopic
                if ('<' in subtopic_name) or ('>' in subtopic_name) or (subtopic_name.strip() == ''): response = -1
                else:
                    atn_db.cur.execute('UPDATE subtopic SET subtopic_name=? WHERE subtopic_id=?', [subtopic_name, int(subtopic_id)])			
                    atn_db.cur.execute('SELECT username FROM user WHERE userid=?',[int(userid)])
                    username, = atn_db.cur.fetchone()
                    atn_db.cur.execute('SELECT topic_name FROM topic WHERE topic_id=?',[int(topic_id)])
                    topic_name, = atn_db.cur.fetchone()
                    try: mylog.log_edit_subtopic(username, topic_id, topic_name, subtopic_id, subtopic_name)
                    except: pass
                    atn_db.commit()
                    response = 1
            else:
                # add subtopic
                if ('<' in subtopic_name) or ('>' in subtopic_name) or (subtopic_name.strip() == ''): response = -1
                else:
                    atn_db.insert('subtopic', [None, subtopic_name, int(topic_id), 0, 0])
                    response = atn_db.cur.lastrowid
			
                    atn_db.cur.execute('SELECT username FROM user WHERE userid=?',[int(userid)])
                    username, = atn_db.cur.fetchone()
                    atn_db.cur.execute('SELECT topic_name FROM topic WHERE topic_id=?',[int(topic_id)])
                    topic_name, = atn_db.cur.fetchone()
                    try: mylog.log_add_subtopic(username, topic_id, topic_name, response, subtopic_name)
                    except: pass

                    atn_db.commit()

        print('Content-Type: text/plain\r\n')
        print(response)

        atn_db.close()

# __main__

form = cgi.FieldStorage()
subtopicHandle(form, environ)

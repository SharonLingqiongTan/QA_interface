#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, sys, datetime
import mylog
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path

def topic_nameCheck(topic_name, topic_id, atn_db):
    atn_db.cur.execute('SELECT topic_name FROM topic WHERE state<2 AND topic_id!=?', [int(topic_id)])
    names = atn_db.cur.fetchall()
    for name, in names:
        if name.lower() == topic_name.lower():
            return True
    return False 
    
def topicHandle(form, environ):

    result = cookieAuthentication(environ)

    if result:

        userid = form.getvalue("userid", None)
        domain_id = form.getvalue("domain_id", None)
        topic_id = form.getvalue("topic_id", '-1')
        topic_name = form.getvalue("topic_name", "")
        topic_name = ' '.join(topic_name.split())

        atn_db  = DBHandler(db_path.atn)

        ## for edit: topic-user matching check
        flag = topic_nameCheck(topic_name, topic_id, atn_db)
        if flag:
            response = 0
        else:
            userid, username, usercookie = result
            atn_db.cur.execute('SELECT domain_name FROM domain WHERE domain_id=?',[domain_id])
            domain_name, = atn_db.cur.fetchone()
            if topic_id != '-1':
                atn_db.cur.execute('SELECT topic_name FROM topic WHERE topic_id=?', [int(topic_id)])
                oname = atn_db.cur.fetchone()
                if oname == '': 
                    response  = -1
                else:
                    # edit topic
                    if ('<' in topic_name) or ('>' in topic_name) or (topic_name.strip() == ''): response = -1
                    else:
                        atn_db.cur.execute('UPDATE topic SET topic_name=? WHERE topic_id=?', [topic_name, int(topic_id)])
                            
                        try: mylog.log_edit_topic(username, domain_id, domain_name, topic_id, topic_name)
                        except: pass
                            
                        atn_db.commit()
                        response = 1 
            else:
                if ('<' in topic_name) or ('>' in topic_name) or (topic_name.strip() == ''): response = -1
            	else:     
                    atn_db.cur.execute('SELECT last_topic_id FROM last_topic WHERE userid=? AND domain_id=?', [int(userid), int(domain_id)])
                    last_topic_id, = atn_db.cur.fetchone()

                    atn_db.cur.execute('SELECT mode, level, para, docno FROM topic WHERE topic_id=?', [last_topic_id])
                    mode, level, para, docno = atn_db.cur.fetchone()

                    atn_db.insert('topic',[None, topic_name, None, int(userid), int(domain_id), mode, level, '', docno, 0])
                    response = atn_db.cur.lastrowid

                    para = para.replace('T='+str(last_topic_id), 'T='+str(response))

                    atn_db.cur.execute('UPDATE topic SET para=? WHERE topic_id=?', [para,response])

                    try: mylog.log_add_topic(username, domain_id, domain_name, response, topic_name)
                    except: pass

                    atn_db.commit()

        print('Content-Type: text/plain\r\n')
        print(response)

        atn_db.close()


# __main__

form = cgi.FieldStorage()
topicHandle(form, environ)

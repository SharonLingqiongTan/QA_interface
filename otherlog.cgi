#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog

def logHandle(form, environ):

    result = cookieAuthentication(environ)
    if not result: return

    userid, username, usercookie = result

    topic_id = form.getvalue('topic_id', None)
    docno = form.getvalue('docno', None)
    mode = form.getvalue('source', None)
    rank = form.getvalue('rank', None)
    flag = form.getvalue('flag')
    type = form.getvalue('type',None)
    query = form.getvalue('query', None)
    hstring = form.getvalue('hstring',None)
    color = form.getvalue('color', None)
    subtopic_id = form.getvalue('subtopic_id', None)

    if mode == 'L': source = 'lemur'
    elif mode == 'S': source = 'solr'
    elif mode == 'T': source = 'terrier'
    elif mode == 'G': source = 'pink_findmore'
    elif mode == 'N': source = 'blue_findmore'
    else: source = 'unknown'

    if flag == 'logout':
        try: mylog.log_logout(username)
        except: pass
    elif flag == 'click':
        try: mylog.log_click_into_doc(username, topic_id, docno, source)
        except: pass
    elif flag == 'goback':
        try: mylog.log_goback_to_list(username, topic_id, docno, source)
        except: pass
    elif flag == 'highlight':
        try: mylog.log_highlight(username, topic_id, docno, hstring)
        except: pass
    elif flag == 'list':
        atn_db = DBHandler(db_path.atn)
        atn_db.cur.execute('SELECT docno FROM search_list WHERE topic_id=?', [int(topic_id)])
        docs = atn_db.cur.fetchall()
        atn_db.cur.execute('''
            SELECT COUNT(1) FROM search_list, filter_list 
            WHERE search_list.topic_id = filter_list.topic_id
            AND search_list.docno = filter_list.docno
            AND search_list.topic_id = ?
            AND filter_list.state = 1
        ''', [int(topic_id)])
        num_of_tagged, = atn_db.cur.fetchone()
        mylog.log_list(username, docs, len(docs), num_of_tagged)
        #except: pass
        atn_db.close()
    elif flag == 'query':
        atn_db = DBHandler(db_path.atn)
	a = open("query.txt","w")
	a.write(query)
	a.close()
        atn_db.cur.execute('SELECT topic_name FROM topic WHERE topic_id=?', [int(topic_id)])
        topic_name, = atn_db.cur.fetchone()
	atn_db.cur.execute('UPDATE topic SET para=? WHERE topic_id=?', ["T="+topic_id+"&q="+query,int(topic_id)])
        atn_db.commit()
	try: mylog.log_query(username, source, topic_id, topic_name, query)
        except: pass
        atn_db.close()
    elif flag == 'findmore':
        atn_db = DBHandler(db_path.atn)
        atn_db.cur.execute('SELECT subtopic_name FROM subtopic WHERE subtopic_id=?', [int(subtopic_id)])
        subtopic_name, = atn_db.cur.fetchone()
        try: mylog.log_findmore(username, color, topic_id, subtopic_id, subtopic_name)
        except: pass
        atn_db.close()
    elif flag == 'help':
        try: mylog.log_help(username, type)
        except: pass
    elif flag == 'others':
        try: mylog.log_other(username, type)
        except: pass
    elif flag == 'finish':
        try: mylog.log_finish(username, topic_id)
        except: pass


    #elif flag == 'finish':
    #    dh.write('topic/finish  |  time: %s  |  # of fields: 1  |  topic_id: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id))
    #elif flag == 'download':
    #    dh.write('download  |  time: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"))) 

    print('status: 200 OK\r\n')

form = cgi.FieldStorage()
logHandle(form, environ)

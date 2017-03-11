#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler
from authentication import cookieAuthentication
from config import db_path
from os import environ
import postNugget
import mylog

def moveHandle(form, environ):
    result = cookieAuthentication(environ)

    if not result: return

    userid, username, usercookie = result

    topic_id = int(form.getvalue("topic_id"))
    docno = form.getvalue("docno")
    signal = form.getvalue("signal")

    atn_db  = DBHandler(db_path.atn)

    print("Content-Type: text/plain\r\n")

    # add the doc to filter_list as discarded doc
    if signal in ['r','d']:
        atn_db.cur.execute('SELECT * FROM filter_list WHERE topic_id=? AND docno=?', [topic_id, docno])
        exist_check = atn_db.cur.fetchone()
        if not exist_check:
            atn_db.insert('filter_list',[topic_id, docno, ['r','d'].index(signal)+2])
            atn_db.commit()
        else:
            print('-1')
            atn_db.close()
            return

        atn_db.cur.execute('SELECT userid, topic_name, domain_id FROM topic WHERE topic_id=?',[topic_id])
        userid, topic_name, domain_id= atn_db.cur.fetchone()
        
        corpus = ['EBOLA', 'POLAR', 'WEAPON'][domain_id-1]
        if signal == 'd': cmd = 'DUPLICATE'
        else: cmd = 'IRRELEVANT'
        m1 = m2 = ''
        try: 
            m1, m2 = postNugget.discardDoc(userid, topic_id, corpus, cmd, docno)
        except: 
            pass

        try: mylog.log_discard_doc(username, cmd.lower(), str(topic_id), docno)
        except: pass
    
    table = 'search_list' 

    if signal == 'p':
        atn_db.cur.execute('SELECT row_num, docno FROM %s WHERE topic_id=? AND row_num < (SELECT row_num FROM %s WHERE topic_id=? AND docno=?) ORDER BY row_num DESC LIMIT 1'%(table, table), [topic_id, topic_id, docno])
        try: mylog.log_prev_doc(username, str(topic_id), docno)
        except: pass
    else:
        atn_db.cur.execute('SELECT row_num, docno FROM %s WHERE topic_id=? AND row_num > (SELECT row_num FROM %s WHERE topic_id=? AND docno=?) LIMIT 1'%(table, table), [topic_id, topic_id, docno])
        if signal == 'n':
            try: mylog.log_next_doc(username, str(topic_id), docno)
            except: pass

    tmpresult = atn_db.cur.fetchone()

    if signal in ['d','r']:
        atn_db.cur.execute('DELETE FROM search_list WHERE topic_id=? AND docno=?',[topic_id, docno])
        atn_db.commit()

    if tmpresult: 
        row_num, nextdoc = tmpresult
        print(nextdoc)
        # update topic last doc
        atn_db.cur.execute('UPDATE topic SET docno=? WHERE topic_id=?', [nextdoc, topic_id])
        atn_db.commit()
    else: 
        print("0")  

    atn_db.close()

# __main__

form = cgi.FieldStorage()
moveHandle(form, environ)


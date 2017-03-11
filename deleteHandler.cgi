#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3, datetime
from database import DBHandler
from authentication import cookieAuthentication
from os import environ
from config import db_path
import mylog
import postNugget

def deleteHandle(form, environ):
    result = cookieAuthentication(environ)
    if result:
        userid, username, usercookie = result

        signal = form.getvalue("signal", '2')
        passage_id = form.getvalue("passage_id", None)
        subtopic_id = form.getvalue("subtopic_id", None)
        topic_id = form.getvalue("topic_id", None)
        userid = form.getvalue("userid", None)
        domain_id = form.getvalue("domain_id", None)

        atn_db = DBHandler(db_path.atn)

        if passage_id:

            topic_id = int(topic_id)

            atn_db.cur.execute('UPDATE passage SET state=? WHERE passage_id=?',[int(signal), int(passage_id)])

            atn_db.cur.execute('SELECT userid, domain_id FROM topic WHERE topic_id=?',[topic_id])
            userid, domain_id= atn_db.cur.fetchone()
            atn_db.cur.execute('SELECT username FROM user WHERE userid=?',[userid])
            username, = atn_db.cur.fetchone()
            atn_db.cur.execute('SELECT subtopic_id, docno, passage_name FROM passage WHERE passage_id=?',[int(passage_id)])
            subtopic_id, docno, passage_name = atn_db.cur.fetchone()

            atn_db.cur.execute('''
                DELETE FROM filter_list WHERE topic_id=? AND docno=? AND
                (SELECT COUNT(1) FROM subtopic, passage
                WHERE subtopic.subtopic_id = passage.subtopic_id
                AND subtopic.topic_id = ?
                AND subtopic.state = 0
                AND passage.state = 0
                AND passage.docno = ?) = 0
            ''', [topic_id, docno, topic_id, docno])
            atn_db.commit()

            corpus = ['EBOLA', 'POLAR', 'WEAPON'][domain_id-1]
            reason = ['I','D'][int(signal)-2]
            m1 = m2 = ''
            try: 
                m1, m2 = postNugget.deleteNugget(userid, topic_id, subtopic_id, corpus, int(passage_id), reason)
            except: 
                pass

            try: mylog.log_delete_passage(username, signal, passage_id, passage_name)
            except: pass

            print("Status: 200 OK\r\n")

        elif subtopic_id:
            atn_db.cur.execute('UPDATE subtopic SET state=1 WHERE subtopic_id=?',[int(subtopic_id)])

            atn_db.cur.execute('''
                DELETE FROM filter_list WHERE docno NOT IN
                (SELECT DISTINCT passage.docno FROM subtopic, passage 
                WHERE subtopic.subtopic_id = passage.subtopic_id
                AND subtopic.topic_id = (SELECT topic_id FROM subtopic WHERE subtopic_id=?)
                AND subtopic.state = 0
                AND passage.state = 0) AND topic_id=(SELECT topic_id FROM subtopic WHERE subtopic_id=?) AND state=1
            ''', [int(subtopic_id), int(subtopic_id)])
            atn_db.commit()
            
            atn_db.cur.execute('SELECT subtopic_name FROM subtopic WHERE subtopic_id=?',[int(subtopic_id)])
            subtopic_name, = atn_db.cur.fetchone()

            try: mylog.log_delete_subtopic(username, subtopic_id)
            except: pass

            print("Status: 200 OK\r\n")

        elif topic_id:
            atn_db.cur.execute('SELECT topic_name, domain_id FROM topic WHERE topic_id=?',[int(topic_id)])
            topic_name, domain_id = atn_db.cur.fetchone()
            if topic_name == '': 
                print('Content-Type: text/plain\r\n')
                print(topic_id) 
                atn_db.close()
                return

            atn_db.cur.execute('UPDATE topic SET state=2 WHERE topic_id=?',[int(topic_id)])
            
            atn_db.cur.execute('SELECT topic_id FROM topic WHERE domain_id=? AND userid=? AND state!=2 ORDER BY topic_id DESC LIMIT 1',[int(domain_id), int(userid)])
            next_topic_id, = atn_db.cur.fetchone()
            
            atn_db.cur.execute('UPDATE last_topic SET last_topic_id=? WHERE userid=? AND domain_id=?', [next_topic_id, int(userid), int(domain_id)])

            try: mylog.log_delete_topic(username, domain_id, topic_id)
            except: pass

            atn_db.commit()
            print('Content-Type: text/plain\r\n')
            print(next_topic_id)

        atn_db.close()

form = cgi.FieldStorage()
deleteHandle(form, environ)

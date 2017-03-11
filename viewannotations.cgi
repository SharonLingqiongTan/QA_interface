#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler
from authentication import cookieAuthentication
from os import environ

def viewannotations(form, environ):
    userid = form.getvalue("userid")
    username = form.getvalue("username")
    atn_db = DBHandler("./database/test.db")

    result = cookieAuthentication(environ)
    if result:
        fh = open('./view/'+username+'.csv','w')
        fh.write('domain_id,domain_name,userid,username,topic_id,topic_name,subtopic_id,subtopic_name,passage_id,passage_name,docno,offset_start,offset_end,grade,timestamp\r\n')
	atn_db.cur.execute('SELECT topic_id, topic_name, domain_id FROM topic WHERE userid=? AND state!=2', [int(userid)])
        topics = atn_db.cur.fetchall()
	for topic_id, topic_name, domain_id in topics:
	    if topic_name == "": continue
            atn_db.cur.execute('SELECT domain_name FROM domain WHERE domain_id=?', [domain_id])
            domain_name, = atn_db.cur.fetchone()
            atn_db.cur.execute('SELECT subtopic_id, subtopic_name FROM subtopic WHERE topic_id=? AND state=0', [topic_id])
            subtopics = atn_db.cur.fetchall()
	    if len(subtopics) == 0:
		atn_db.cur.execute('SELECT create_time FROM topic WHERE topic_id=?',[topic_id])
		timestamp, = atn_db.cur.fetchone()
		tmplist = [str(domain_id), domain_name, str(userid), username, str(topic_id), topic_name, ' ', ' ', ' ', ' ', ' ', ' ', ' ' , ' ', timestamp, '\r\n']
		for i in range(len(tmplist)):
		    tmplist[i] = ((tmplist[i].encode('UTF-8')).replace(',',' ')).replace('\n',' ')
		fh.write(','.join(tmplist) + '\r\n')
            for subtopic_id, subtopic_name in subtopics:
                atn_db.cur.execute('SELECT passage_id, passage_name, docno, offset_start, offset_end, grade, create_time FROM passage WHERE subtopic_id=? AND state !=2', [subtopic_id,])
		passages = atn_db.cur.fetchall()
		if len(passages) == 0:
		    atn_db.cur.execute('SELECT create_time FROM subtopic WHERE subtopic_id=?',[subtopic_id])
		    timestamp, = atn_db.cur.fetchone()
		    passages = [[' ']*6]
		    passages[0].append(timestamp)
		for passage in passages:
                    #print str(passage[6].encode('UTF-8'))
		    tmplist = [str(domain_id), domain_name, str(userid), username, str(topic_id), topic_name, str(subtopic_id), subtopic_name, str(passage[0]), passage[1], passage[2], str(passage[3]), str(passage[4]), str(passage[5]), str(passage[6]), '\r\n']
                    tmplist2 = []
                    for item in tmplist:
                        itemstr = item.encode('UTF-8')
                        itemstr = itemstr.replace(',',' ')
                        itemstr = itemstr.replace('\n',' ')
                        tmplist2.append(itemstr)
		    if tmplist2[-2] == '-1'.encode('UTF-8'):
			tmplist2[-2] = ' '.encode('UTF-8')
		    fh.write(','.join(tmplist2) + '\r\n')
        fh.close()
	print("Status: 200 OK\r\n")
    atn_db.close()

form = cgi.FieldStorage()
viewannotations(form, environ)

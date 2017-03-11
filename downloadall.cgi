#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler

def viewannotations():
    atn_db = DBHandler("./database/test.db")

    fh = open('./view/all.csv','w')
    fh.write('domain_id,domain_name,userid,username,topic_id,topic_name,subtopic_id,subtopic_name,passage_id,passage_name,docno,offset_start,offset_end,grade,timestamp\r\n')

    for userid in range(1,7):
        atn_db.cur.execute('SELECT username FROM user WHERE userid=?',[userid])
        username, = atn_db.cur.fetchone()
	atn_db.cur.execute('SELECT topic_id, topic_name, domain_id FROM topic WHERE userid=? AND state!=2', [int(userid)])
        topics = atn_db.cur.fetchall()
	for topic_id, topic_name, domain_id in topics:
	    if topic_name == "": continue
	    if '"' in topic_name: print 'topic', topic_id, topic_name
            atn_db.cur.execute('SELECT domain_name FROM domain WHERE domain_id=?', [domain_id])
            domain_name, = atn_db.cur.fetchone()
            atn_db.cur.execute('SELECT subtopic_id, subtopic_name FROM subtopic WHERE topic_id=? AND state=0', [topic_id])
            subtopics = atn_db.cur.fetchall()
	    if len(subtopics) == 0:
		continue
            for subtopic_id, subtopic_name in subtopics:
		if '"' in subtopic_name: print 'subtopic', subtopic_id, subtopic_name
                atn_db.cur.execute('SELECT passage_id, passage_name, docno, offset_start, offset_end, grade, create_time FROM passage WHERE subtopic_id=? AND state <=1', [subtopic_id,])
		passages = atn_db.cur.fetchall()
		if len(passages) == 0:
		    continue
		for passage in passages:
                    #print str(passage[6].encode('UTF-8'))
		    tmplist = [str(domain_id), domain_name, str(userid), username, str(topic_id), topic_name, str(subtopic_id), subtopic_name, str(passage[0]), passage[1], passage[2], str(passage[3]), str(passage[4]), str(passage[5]), str(passage[6]), '\r\n']
                    tmplist2 = []
                    for item in tmplist:
                        itemstr = item.encode('UTF-8')
                        itemstr = itemstr.replace(',',' ')
                        itemstr = itemstr.replace('\n',' ')
			itemstr = itemstr.replace('"',' ')
                        tmplist2.append(itemstr)
		    if tmplist2[-2] == '-1'.encode('UTF-8'):
			tmplist2[-2] = ' '.encode('UTF-8')
		    fh.write(','.join(tmplist2) + '\r\n\r\n\r\n')
    fh.close()
    atn_db.close()

viewannotations()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, sqlite3
from database import DBHandler

def viewsummary():
    atn_db = DBHandler("./database/test.db")

    if True:
        fh = open('./view/summary.csv','w')
        fh.write('domain_id,domain_name,userid,username,topic_id,topic_name,subtopic_id,subtopic_name,passage_id,passage_name,docno,offset_start,offset_end,grade,timestamp\n\n\n')
	atn_db.cur.execute('SELECT userid, topic_id, topic_name, domain_id FROM topic WHERE state!=2')
        topics = atn_db.cur.fetchall()
	for userid, topic_id, topic_name, domain_id in topics:
	    if userid>6: continue
	    atn_db.cur.execute('SELECT username FROM user WHERE userid=?', [userid])
	    username, =atn_db.cur.fetchone()
            atn_db.cur.execute('SELECT domain_name FROM domain WHERE domain_id=?', [domain_id])
            domain_name, = atn_db.cur.fetchone()
            atn_db.cur.execute('SELECT subtopic_id, subtopic_name FROM subtopic WHERE topic_id=? AND state=0', [topic_id])
            subtopics = atn_db.cur.fetchall()
	    if len(subtopics) == 0:
		continue
            for subtopic_id, subtopic_name in subtopics:
                atn_db.cur.execute('SELECT passage_id, passage_name, docno, offset_start, offset_end, grade, create_time FROM passage WHERE subtopic_id=? AND state<=1', [subtopic_id,])
		passages = atn_db.cur.fetchall()
		if len(passages) == 0:
		    continue
		for passage in passages:
                    #print str(passage[6].encode('UTF-8'))
		    tmplist = [str(domain_id), domain_name, str(userid), username, str(topic_id), topic_name, str(subtopic_id), subtopic_name, str(passage[0]), passage[1], passage[2], str(passage[3]), str(passage[4]), str(passage[5]), str(passage[6])]
                    tmplist2 = []
                    for item in tmplist:
                        itemstr = item.encode('UTF-8')
                        itemstr = itemstr.replace(',',' ')
                        itemstr = itemstr.replace('\n',' ')
                        itemstr = itemstr.replace('\r',' ')
			itemstr = itemstr.replace('"',' ')
                        tmplist2.append(itemstr)
		    fh.write(','.join(tmplist2) + '\n\n\n\n')
        fh.close()
    atn_db.close()

viewsummary()

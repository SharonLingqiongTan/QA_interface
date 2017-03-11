#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from database import DBHandler

def escapeString(string):
    string = string.replace('<', '&lt;').replace('>','%gt;')
    string = string.replace('"', '&quot;').replace("'",'&apos;')
    string = string.replace('&', "&amp;")
    return string

dh = open('groundtruth.xml','w')
atn_db  = DBHandler("./database/test.db")
atn_db.cur.execute('SELECT domain_id, domain_name FROM domain WHERE domain_id<=3')
domains = atn_db.cur.fetchall()
dh.write('<trec_dd>\n')
topic_counter = 0
subtopic_counter = 0
t2 = '\t' * 2
t3 = '\t' * 3
t4 = '\t' * 4 
t5 = '\t' * 5
for domain in domains:
    domain_id, domain_name = domain
    atn_db.cur.execute('SELECT topic_id, topic_name FROM topic WHERE domain_id=? AND userid<=6 AND state!=2',[domain_id])
    topics = atn_db.cur.fetchall()
    topic_counter += len(topics)
    dh.write('\t<domain name="%s" id="%s" num_of_topics="%s">\n'%(domain_name, str(domain_id), str(len(topics)))) 
    for topic in topics:
	topic_id, topic_name = topic
	atn_db.cur.execute('SELECT subtopic_id, subtopic_name FROM subtopic WHERE topic_id=? AND state!=1',[topic_id])
	subtopics = atn_db.cur.fetchall()
	subtopic_counter += len(subtopics)
	dh.write('%s<topic name="%s" id="%s" num_of_subtopics="%s">\n'%(t2, escapeString(topic_name), str(topic_id), str(len(subtopics))))
	for subtopic in subtopics:
	    subtopic_id, subtopic_name = subtopic
	    atn_db.cur.execute('SELECT passage_id, passage_name, docno, grade FROM passage WHERE subtopic_id=? AND state!=2 AND grade>0',[subtopic_id])
	    passages = atn_db.cur.fetchall()
	    dh.write('%s<subtopic name="%s" id="%s" num_of_passages="%s">\n'%(t3, escapeString(subtopic_name), str(subtopic_id),str(len(passages))))
	    for passage in passages:
		passage_id, passage_name, docno, grade = passage
		dh.write('%s<passage id="%s">\n%s<docno>%s</docno>\n%s<rating>%s</rating>\n'%(t4, str(passage_id), t5, docno, t5, grade))
		dh.write('%s<text>%s</text>\n%s</passage>\n'%(t5, escapeString(passage_name.encode('utf-8')), t4))
		#dh.write(t4 + '</passage>\n')
	    dh.write('%s</subtopic>\n'%t3)
	dh.write('%s</topic>\n'%t2)
    dh.write('\t</domain>\n')
dh.write('</trec_dd>')
dh.close()
print '# of topics:', topic_counter
print '# of subtopics:', subtopic_counter

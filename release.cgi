#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from database import DBHandler

dh = open('subtopic_stat.xml','w')
atn_db  = DBHandler("./database/test.db")
atn_db.cur.execute('SELECT domain_id, domain_name FROM domain WHERE domain_id<=3')
domains = atn_db.cur.fetchall()
dh.write('<trec_dd>\n')
topic_counter = 0
subtopic_counter = 0
for domain in domains:
    domain_id, domain_name = domain
    dh.write('\t<domain>\n\t\t<domain_name>%s</domain_name>\n'%domain_name) 
    atn_db.cur.execute('SELECT topic_id, topic_name FROM topic WHERE domain_id=? AND userid<=6 AND state!=2',[domain_id])
    topics = atn_db.cur.fetchall()
    topic_counter += len(topics)
    dh.write('\t\t<number_of_topics>%s</number_of_topics>\n\t\t<topics>\n'%str(len(topics)))
    for topic in topics:
	topic_id, topic_name = topic
	dh.write('\t\t\t<topic>\n\t\t\t\t<topic_name>%s</topic_name>\n'%topic_name)
	atn_db.cur.execute('SELECT subtopic_id, subtopic_name FROM subtopic WHERE topic_id=? AND state!=1',[topic_id])
	subtopics = atn_db.cur.fetchall()
	subtopic_counter += len(subtopics)
	dh.write('\t\t\t\t<number_of_subtopics>%s</number_of_subtopics>\n\t\t\t\t<subtopics>\n'%str(len(subtopics)))
	for subtopic in subtopics:
	    subtopic_id, subtopic_name = subtopic
	    dh.write('\t\t\t\t\t<subtopic>\n\t\t\t\t\t\t<subtopic_name>%s</subtopic_name>\n\t\t\t\t\t</subtopic>\n'%subtopic_name)
	dh.write('\t\t\t\t</subtopics>\n\t\t\t</topic>\n')
    dh.write('\t\t</topics>\n\t</domain>\n')
dh.write('</trec_dd>')
dh.close()
print '# of topics:', topic_counter
print '# of subtopics:', subtopic_counter

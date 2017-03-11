#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3, sys
from os import getcwd
sys.path.append(getcwd() + '/../')
from database import DBHandler


atn_db = DBHandler('../database/test.db')
atn_db.cur.execute('SELECT COUNT(1) FROM topic, filter_list WHERE filter_list.topic_id=topic.topic_id AND topic.userid<=6 AND topic.state=0 AND filter_list.state=1')
rcount, = atn_db.cur.fetchone()
atn_db.cur.execute('SELECT COUNT(1) FROM topic, filter_list WHERE filter_list.topic_id=topic.topic_id AND topic.userid<=6 AND topic.state=0 AND filter_list.state=2')
ircount, = atn_db.cur.fetchone()
atn_db.cur.execute('SELECT COUNT(1) FROM topic, filter_list WHERE filter_list.topic_id=topic.topic_id AND topic.userid<=6 AND topic.state=0 AND filter_list.state=3')
dcount, = atn_db.cur.fetchone()
string = "<div>total doc: %d |  relevant doc: %d | irrelevant doc: %d | duplicate doc: %d</div>"%(rcount+ircount+dcount, rcount, ircount, dcount)
Rarray = ["marginally relevant", "relevant", "highly relevant", "key result"]
for i in range(1,7):
    atn_db.cur.execute('SELECT COUNT(1) FROM topic, filter_list WHERE filter_list.topic_id=topic.topic_id AND topic.userid=? AND topic.state=0 AND filter_list.state=1', [i])
    rcount, = atn_db.cur.fetchone()
    atn_db.cur.execute('SELECT COUNT(1) FROM topic, filter_list WHERE filter_list.topic_id=topic.topic_id AND topic.userid=? AND topic.state=0 AND filter_list.state=2', [i])
    ircount, = atn_db.cur.fetchone()
    atn_db.cur.execute('SELECT COUNT(1) FROM topic, filter_list WHERE filter_list.topic_id=topic.topic_id AND topic.userid=? AND topic.state=0 AND filter_list.state=3', [i])
    dcount, = atn_db.cur.fetchone()
    string += "<li><span class='entypo-folder'>User: %s  | relevant doc: %d | irrelevant doc: %d | duplicate doc: %d</span>\n"%("assr"+str(i), rcount, ircount, dcount)
    string += "<ul>\n"
    for j in range(1,4):
        atn_db.cur.execute('SELECT domain_name, domain_url FROM domain WHERE domain_id=?', [j])
        domain_name, domain_url = atn_db.cur.fetchone()
        string += "<li class='domain' data-url='%s'><span class='entypo-folder'>Domain: %s</span>\n"%(domain_url, domain_name)
        string += "<ul>\n"
        atn_db.cur.execute('SELECT topic_id, topic_name FROM topic WHERE userid=? AND state!=2 AND domain_id=?',[i, j])
        topics = atn_db.cur.fetchall()
        for (topic_id, topic_name) in topics:
            if topic_name == '': continue
            atn_db.cur.execute('SELECT COUNT(1) FROM filter_list WHERE topic_id=? AND state=1', [int(topic_id)])
            rcount, = atn_db.cur.fetchone()
            atn_db.cur.execute('SELECT COUNT(1) FROM filter_list WHERE topic_id=? AND state=2', [int(topic_id)])
            ircount, = atn_db.cur.fetchone()
            atn_db.cur.execute('SELECT COUNT(1) FROM filter_list WHERE topic_id=? AND state=3', [int(topic_id)])
            dcount, = atn_db.cur.fetchone()
            string += "<li><span class='entypo-folder'>Topic: %s (topic_id : %s) | relevant doc: %d | irrelevant doc: %d | duplicate doc: %d</span>\n"%(topic_name, str(topic_id), rcount, ircount, dcount)
            string += "<ul>\n"
            atn_db.cur.execute('SELECT subtopic_id, subtopic_name FROM subtopic WHERE topic_id=? AND state!=1',[topic_id])
            subtopics = atn_db.cur.fetchall()
            for (subtopic_id, subtopic_name) in subtopics:
                atn_db.cur.execute('SELECT COUNT(1) FROM passage WHERE subtopic_id=? AND state=0',[subtopic_id])
                pcount, = atn_db.cur.fetchone()
                string += "<li><span class='entypo-folder subtopic-load' data-subid='%s'>Subtopic: %s (subtopic_id : %s)</span> <span># of nuggets: %d</span>\n"%(str(subtopic_id), subtopic_name, str(subtopic_id), pcount)
                string += "<ul>\n"
                '''
                atn_db.cur.execute('SELECT passage_name, docno, grade FROM passage WHERE subtopic_id=? AND state<=2',[subtopic_id])
                passages = atn_db.cur.fetchall()
                for (passage_name, docno, score) in passages:
                    if score == 0:
                        relevance = "not judged yet"
                    else:
                        relevance = Rarray[score - 1]
                    string += "<li><span class='entypo-newspaper'></span> <span class='docno'>%s</span> <span class='score'> | %s | </span>%s</li>\n"%(docno, relevance, passage_name)
                '''
                string += "</ul>\n"
                string += "</li>\n"
            string += "</ul>\n"
            string += "</li>\n"
        string += "</ul>\n"
        string += "</li>\n"
    string += "</ul>\n"
    string += "</li>\n"

fh = open("admin.html","r")
print("Content-Type: text/html\r\n")
p = fh.read()
print((string.encode('utf-8')).join(p.split('%s')))
fh.close()
atn_db.close()

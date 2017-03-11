#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3, sys
from os import getcwd
sys.path.append(getcwd() + '/../')
from database import DBHandler

atn_db = DBHandler('../database/test.db')
string = ""
Rarray = ["marginally relevant", "relevant", "highly relevant", "key result"]
for i in range(1,7):
    string += "<li><span class='entypo-folder'>User: %s</span>\n"%("assr"+str(i))
    string += "<ul>\n"
    for j in range(1,4):
        atn_db.cur.execute('SELECT domain_name, domain_url FROM domain WHERE domain_id=?', [j])
        domain_name, domain_url = atn_db.cur.fetchone()
        string += "<li class='domain' data-url='%s'><span class='entypo-folder'>Domain: %s</span>\n"%(domain_url, domain_name)
        string += "<ul>\n"
        atn_db.cur.execute('SELECT topic_id, topic_name, state FROM topic WHERE userid=? AND domain_id=?',[i, j])
        topics = atn_db.cur.fetchall()
        for (topic_id, topic_name, state) in topics:
            if topic_name == '': continue
            if state !=2:
                string += "<li><span class='entypo-folder'>Topic: %s (topic_id : %s)</span>\n"%(topic_name, str(topic_id))
            else:
                string += "<li><span class='entypo-folder'>Topic: %s (topic_id : %s) | <span class='deleted'> deleted </span></span>\n"%(topic_name, str(topic_id))	
            string += "<ul>\n"
            atn_db.cur.execute('SELECT subtopic_id, subtopic_name, state FROM subtopic WHERE topic_id=?',[topic_id])
            subtopics = atn_db.cur.fetchall()
            for (subtopic_id, subtopic_name, state) in subtopics:
                if state !=1:
                    string += "<li><span class='entypo-folder subtopic-load' data-subid='%s'>Subtopic: %s (subtopic_id : %s)</span>\n"%(str(subtopic_id), subtopic_name, str(subtopic_id))
                else:
                    string += "<li><span class='entypo-folder subtopic-load' data-subid='%s'>Subtopic: %s (subtopic_id : %s) | <span class='deleted'> deleted </span></span>\n"%(str(subtopic_id), subtopic_name, str(subtopic_id))
                string += "<ul>\n"
                '''
                atn_db.cur.execute('SELECT passage_name, docno, grade FROM passage WHERE subtopic_id=? AND state!=2',[subtopic_id])
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

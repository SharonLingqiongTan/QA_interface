#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3, sys, cgi, os
from os import getcwd
sys.path.append(getcwd() + '/../')
from database import DBHandler

form = cgi.FieldStorage()
subtopic_id =  form.getvalue("subtopic_id", None)

if subtopic_id:
    Rarray = ["marginally relevant", "relevant", "highly relevant", "key result"]
    atn_db = DBHandler('../database/test.db')
    string = ""
    atn_db.cur.execute('SELECT passage_name, docno, grade, state FROM passage WHERE subtopic_id=?',[int(subtopic_id)])
    passages = atn_db.cur.fetchall()
    for (passage_name, docno, score, state) in passages:
        if score == 0:
            relevance = "not judged yet"
        else:
            relevance = Rarray[score - 1]
        if state <=2:
            string += "<li><span class='entypo-newspaper'></span> <span class='docno'>%s</span> <span class='score'> | %s | </span>%s</li>\n"%(docno, relevance, passage_name)
        elif 'records.cgi' in os.environ['HTTP_REFERER']:
            string += "<li><span class='entypo-newspaper'></span> <span class='docno'>%s</span> <span class='score'> | %s | <span class='deleted'>deleted | </span></span>%s</li>\n"%(docno, relevance, passage_name)
	    
    print('Content-Type: text/plain\r\n')
    print(string.encode('UTF-8'))

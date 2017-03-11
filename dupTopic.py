#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3, sys
from database import DBHandler

def dupTopic():

    userid = 30 
    topic_id = 391
    # copy this topic to this userid

    atn_db  = DBHandler('./database/test.db')
    atn_db.insert('topic', [None, "slums and orphans _ debug", None, userid, 1, 'L', 'L', '', '', 0])
    new_tid = atn_db.cur.lastrowid

    atn_db.cur.execute('SELECT * FROM subtopic WHERE topic_id=? AND state=0', [topic_id])
    subtopics = atn_db.cur.fetchall()
    for subtopic in subtopics:
        atn_db.insert('subtopic', [None, subtopic[1] + ' _ debug', new_tid, 0, 0])
        new_sid = atn_db.cur.lastrowid
        atn_db.cur.execute('SELECT * FROM passage WHERE subtopic_id=? AND state=0', [subtopic[0]])
        passages = atn_db.cur.fetchall()
        for passage in passages:
            atn_db.insert('passage', [None, passage[1], passage[2], 0, 0, passage[5], new_sid, 0])
    
    atn_db.cur.execute('SELECT docno, state FROM filter_list WHERE topic_id=?', [topic_id])
    
    fdocs = atn_db.cur.fetchall()
    
    for fdoc in fdocs:
        docno, state = fdoc
        atn_db.insert('filter_list',[new_tid, docno, state])

    atn_db.commit()
    atn_db.close()

dupTopic()

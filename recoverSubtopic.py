#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3, sys
from database import DBHandler

def recoverSubtopic():

    subtopic_id = int(sys.argv[1])
    atn_db  = DBHandler('./database/test.db')
    atn_db.cur.execute('UPDATE subtopic SET state=0 WHERE subtopic_id=?', [subtopic_id])
    atn_db.cur.execute(
        '''
        UPDATE filter_list SET state=1 
        WHERE topic_id = (SELECT topic_id FROM subtopic WHERE subtopic_id=?)
        AND docno IN (
        SELECT DISTINCT passage.docno FROM passage
        WHERE passage.subtopic_id=?
        AND passage.state=0) AND state!=1
        ''',[subtopic_id, subtopic_id])
    atn_db.cur.execute(
        '''
        INSERT INTO filter_list (topic_id, docno, state)
        SELECT DISTINCT subtopic.topic_id, passage.docno, 1 FROM subtopic, passage
        WHERE subtopic.subtopic_id = passage.subtopic_id
        AND subtopic.subtopic_id=?
        AND passage.state = 0
        AND passage.docno NOT in (SELECT docno FROM filter_list WHERE topic_id = subtopic.topic_id); 
        ''', [subtopic_id])
    atn_db.commit()
    atn_db.close()

recoverSubtopic()

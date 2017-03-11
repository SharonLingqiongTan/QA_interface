#!/usr/bin/python
# -*- coding: utf-8 -*-

from database import *
from config import db_path, domains
import sys
import os

def initTopic(userid, domain_id, atn_db):
    atn_db.insert('topic', [None, '', None, int(userid), int(domain_id), 'L', 'L', '', '', 0])
    return atn_db.cur.lastrowid

if len(sys.argv) == 1:
    # create databases(atnDB, userDB) and tables
    atn_db = DBHandler(db_path.atn, 1)
    atn_tables = AtnTables()
    os.chmod(db_path.atn, 0777)
    atn_db.createTables(atn_tables.getTables())

    user_db = DBHandler(db_path.user, 1)
    user_tables = UserTables()
    user_db.createTables(user_tables.getTables())


    # setup domains
    for domain in domains:
        atn_db.insert('domain', [domain['id'], domain['name'], domain['url']])

    atn_db.commit()
    user_db.commit()
    
    for filename in os.listdir('./userlog/'):
        os.remove('./userlog/%s'%filename)
else:
    if len(sys.argv) == 5 and sys.argv[1] == '-u' and sys.argv[3] == '-p':
        # add user
        import hashlib
        m = hashlib.md5()
        atn_db = DBHandler(db_path.atn)
        user_db = DBHandler(db_path.user)
        m.update(sys.argv[2])
        atn_db.insert('user', [None, sys.argv[2], 1, 0])
        user_db.insert('user', [None, sys.argv[2], m.hexdigest(), sys.argv[4]] )
        
        userid = user_db.cur.lastrowid

        for i in range(len(domains)):
            topic_id = initTopic(userid, i+1, atn_db)
            atn_db.insert('last_topic',[userid, i+1, topic_id])

        atn_db.commit()
        user_db.commit()
    else:
        print ('type: -u username -p password')

atn_db.close()
user_db.close()
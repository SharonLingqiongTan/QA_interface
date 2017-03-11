# -*- coding: utf-8 -*-

import sqlite3, os, datetime

class AtnTables:
    def getTables(self):
        return [
            '''
            user(
                userid          INTEGER PRIMARY KEY,
                username        TEXT,
                last_domain_id  INTEGER,
                loption         INTEGER,
                create_time	datetime default current_timestamp
            )
            ''',
            # loption: 0 for showing tagged, 1 for hidding tagged; default 0

            '''
            domain(
                domain_id       INTEGER PRIMARY KEY,
                domain_name     TEXT,
                domain_url      TEXT,
                create_time	datetime default current_timestamp
            )
            ''',

            '''
            last_topic(
                userid          INTEGER,
                domain_id       INTEGER,
                last_topic_id   INTEGER,
                create_time	datetime default current_timestamp,
                PRIMARY KEY(userid, domain_id)
            )
            ''',

            '''
            topic(
                topic_id        INTEGER PRIMARY KEY,
                topic_name      TEXT,
                description     TEXT,
                userid          INTEGER,
                domain_id       INTEGER,
                mode            TEXT,
                level           TEXT,
                para            TEXT,
                docno           TEXT,
                state           INTEGER,
                create_time	datetime default current_timestamp
            )
            ''',
            # mode: S(search) / R(recommend)
            # level: L(list) / D(doc)
            # para: search / recommend query; useful in level in L
            # docno: useful if level in D
            # state:  
            #   originall: 0 created; 1 sent; 2 deleted
            #   new: 0 created; 1 not used; 2 deleted
            '''
            last_list(
                docno           TEXT,
                topic_id        INTEGER,
                snippet         TEXT
            )
            ''',

            '''
            search_list(
                row_num         INTEGER PRIMARY KEY,
                topic_id        INTEGER,
                docno           TEXT
            )
            ''',

            '''
            filter_list(
                topic_id        INTEGER,
                docno           TEXT,
                state           INTEGER,
                create_time datetime default current_timestamp
            )
            ''',
            # state: 1 for tagged, 2 for discarded

            '''
            subtopic(
                subtopic_id     INTEGER PRIMARY KEY,
                subtopic_name   TEXT,
                topic_id        INTEGER,
                scroll_position INTEGER,
                state           INTEGER,
                create_time	datetime default current_timestamp
            )
            ''',
            # state: 0 for created, 1 for deleted
    
            '''
            passage(
                passage_id      INTEGER PRIMARY KEY,
                passage_name    TEXT,
                docno           TEXT,
                offset_start    INTEGER,
                offset_end      INTEGER,
                grade           INTEGER,
                subtopic_id     INTEGER,
                state           INTEGER,
                create_time	datetime default current_timestamp
            )
            '''
            # state: 
            #   originally 0 -> added; ; 1 -> sent; 2 -> deleted
            #   now: 0 -> added; 1-> not used; 2 -> irrelevant deleted; 3-> duplicate deleted
        ]

class UserTables:
    def getTables(self):
        return ['''
                user(
                userid INTEGER PRIMARY KEY,
                username TEXT,
                usercookie TEXT,
                password TEXT,
                create_time	datetime default current_timestamp
                )
                '''
        ]

class DBHandler:

    def __init__(self, dbname, signal=0):
        if signal:
            if os.path.isfile(dbname):
                os.remove(dbname)
        self.conn = sqlite3.connect(dbname,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cur = self.conn.cursor()

    def createTables(self, tables):
        for table in tables:
            self.createTable(table)

    def createTable(self, table):
        self.cur.execute("CREATE TABLE %s"%table)

    def insert(self, table, parameters):
        placeholders = ['?'] * (len(parameters) + 1)
        placeholders_string = ','.join(placeholders)
        parameters.append(datetime.datetime.now())
        self.cur.execute('INSERT INTO %s VALUES(%s)' %(table, placeholders_string), parameters)

    def rollback(self):
        self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

# for doc state:  0-> new; 1->viewed 2->discard 3->completed -1->sent


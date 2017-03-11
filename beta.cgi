#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, cgitb, sqlite3, time, json
import mylog
from os import environ
from database import DBHandler
from authentication import cookieAuthentication, userAuthentication
from config import db_path

def getDomainInfo(userid, username, dict, domain_id, atn_db):

    # get the domain(domain_id/last_domain_id) to show and update last_doamain_id
    if not domain_id:
        atn_db.cur.execute('SELECT last_domain_id FROM user WHERE userid=?', [userid,])
        last_domain_id, = atn_db.cur.fetchone()
    else:
        atn_db.cur.execute('SELECT domain_name FROM domain WHERE domain_id=?',[domain_id,])
        domain_name, = atn_db.cur.fetchone()
        atn_db.cur.execute('UPDATE user SET last_domain_id=? WHERE userid=?', [domain_id, userid])
        
        try: mylog.log_domain(username, domain_id, domain_name)
        except: pass
        
        last_domain_id = int(domain_id)
    dict['domains'].append(last_domain_id)

    # get domain_url
    atn_db.cur.execute('SELECT domain_url FROM domain WHERE domain_id=?', [last_domain_id])
    domain_url, = atn_db.cur.fetchone()
    dict['domains'].append(domain_url)

    # get all domains' ids & urls
    atn_db.cur.execute('SELECT domain_id, domain_name FROM domain')
    domains = atn_db.cur.fetchall()
    for domain in domains:
        dict['domains'].append(domain)

    return last_domain_id

def getTopicInfo(userid, username, dict, topic_id, last_domain_id, atn_db):

    # get the topic to show and update last_topic_id
    if topic_id is None:
        atn_db.cur.execute('SELECT last_topic_id FROM last_topic WHERE userid=? AND domain_id=?', [userid, last_domain_id])
        last_topic_id, = atn_db.cur.fetchone()

        # ?? combine the below select statement with else branch's topic_name select;
        # ?? also consider the log operation
        atn_db.cur.execute('SELECT topic_name FROM topic WHERE topic_id=?',[last_topic_id,])
        topic_name, = atn_db.cur.fetchone()
    else:
        last_topic_id = int(topic_id)

        atn_db.cur.execute('SELECT topic_name FROM topic WHERE topic_id=?',[topic_id,])
        topic_name, = atn_db.cur.fetchone()
        
        try: mylog.log_select_topic(username, topic_id, topic_name)
        except: pass
        
        atn_db.cur.execute('UPDATE last_topic SET last_topic_id=? WHERE userid=? AND domain_id=?', [last_topic_id, userid, last_domain_id])
    
    dict['topics'].append(last_topic_id)
    
    # get topic_info
    atn_db.cur.execute('SELECT mode, level, para, docno, topic_name FROM topic WHERE topic_id=?', [last_topic_id])
    topic_info = list(atn_db.cur.fetchone())
    topic_info[4] = topic_info[4].replace("'",'').replace('"','')
    topic_info[2] = topic_info[2].replace("'",'').replace('"','')
    dict['topics'].extend(topic_info)

    # get topics
    topic_option = ''

    atn_db.cur.execute('SELECT topic_id, topic_name FROM topic WHERE userid=? AND domain_id=? AND state!=2', [userid, last_domain_id])
    topics = atn_db.cur.fetchall()
    for topic in topics:
        if topic[0] == last_topic_id:
            topic_option += "<option value='%s' selected>%s</option>\n"%(str(topic[0]), str(topic[1]))
        else:
            if topic[1] == '': continue
            topic_option += "<option value='%s'>%s</option>\n"%(str(topic[0]), str(topic[1]))

    return topic_option

def printHTML(usercookie, dict, topic_option):
    expires = time.time() + 24 * 3600
    html = open('./html/index.html','r')
    print('Set-Cookie:usercookie=%s;Expires=%s'%(usercookie,time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expires))))
    print('Content-Type: text/html\r\n')
    print(html.read()%("'" + json.dumps(dict) + "'",topic_option))
    html.close()

def loginSuccess((userid, username, usercookie), form):
    domain_id = form.getvalue('domain', None) # string
    topic_id  = form.getvalue('topic' , None) # string

    atn_db = DBHandler(db_path.atn)

    dict = {
            'userid': userid,
            'username': username,
            'domains': [], 
            # current_domain_id, current_domain_url, all domains(domain_id, domain_name)
            'topics': [] 
            # current_topic_id, current_topic_url
        }

    last_domain_id = getDomainInfo(userid, username, dict, domain_id, atn_db)

    topic_option = getTopicInfo(userid, username, dict, topic_id, last_domain_id, atn_db)

    atn_db.cur.execute('SELECT loption FROM user WHERE userid=?', [userid])
    loption, = atn_db.cur.fetchone()
    dict['loption'] = loption

    printHTML(usercookie, dict, topic_option)

    atn_db.commit()
    atn_db.close()

def toLogin(hint=''):
    html = open('./html/login.html','r')
    print('Content-Type: text/html\r\n')
    print(html.read()%hint)
    html.close()

def login(form, envrion):
    flag = False
    result = cookieAuthentication(environ) # result = [userid, username, usercookie] or None
    if result: flag = True
    if not flag:
        username = form.getvalue('username', None)
        password = form.getvalue('password', None)
        if username == None and password == None: hint = ''
        # first time land in this url OR neither username nor password is typed
        else:
            result = userAuthentication(username, password) ## input validation ??
            if result: 
                flag = True
                mylog.log_login(username)
            else: 
                hint = 'invalid username or password'
    if flag: loginSuccess(result, form)
    else: toLogin(hint)

# __main__

#cgitb.enable()
form = cgi.FieldStorage()
login(form, environ)



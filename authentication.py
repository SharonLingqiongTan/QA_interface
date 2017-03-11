# -*- coding: utf-8 -*-
from database import DBHandler
from config import db_path

def cookieAuthentication(env):
    user_db = DBHandler(db_path.user)
    result = None
    if 'HTTP_COOKIE' in env:
        for pair in env['HTTP_COOKIE'].split(';'):
            cookie = pair.strip()
            if cookie.startswith('usercookie'):
                key, value = cookie.split('=')
                user_db.cur.execute('SELECT userid, username, usercookie FROM user WHERE usercookie = ?',[value,])
                result = user_db.cur.fetchone()
                break
    user_db.close()
    return result

def userAuthentication(username, password):
    user_db = DBHandler(db_path.user)
    result = None
    user_db.cur.execute(
        'SELECT userid, username, usercookie FROM user WHERE username = ? AND password = ?',[username, password])
    result = user_db.cur.fetchone()
    user_db.close()
    return result
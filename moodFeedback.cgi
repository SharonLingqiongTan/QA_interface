#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi, datetime
from authentication import cookieAuthentication
from os import environ
import mylog

def feedback(form, environ):
    result = cookieAuthentication(environ)
    if not result: return

    userid, username, usercookie = result

    reason = form.getvalue("reason", None)
    mood = form.getvalue("mood", None)
    mode = form.getvalue("source", None)
    topic_id = form.getvalue("topic_id", None)

    if mode == 'L': source = 'lemur'
    elif mode == 'S': source = 'solr'
    elif mode == 'T': source = 'terrier'
    elif mode == 'G': source = 'pink_findmore'
    elif mode == 'N': source = 'blue_findmore'
    else: source = 'unknown'

    try: mylog.log_mood(username, mood, topic_id, source, reason)
    except: pass

    print("Status: 200 OK\r\n")

# __main__

form = cgi.FieldStorage()
feedback(form, environ)
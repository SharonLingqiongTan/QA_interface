#!/usr/bin/python
# -*- coding: utf-8 -*-
from authentication import cookieAuthentication
from os import environ
import cgi
def moveHandle(form,environ):
    result = cookieAuthentication(environ)
    #a = open("result.txt","w")
    #a.write(str(result))
    #a.close()
    if not result: return
    userid, username, usercookie = result

    topic_id = int(form.getvalue("topic_id"))
    docno = form.getvalue("docno")
    signal = form.getvalue("signal")
    a = open("result.txt","w")
    a.write(docno)
    a.close()
    print("Content-Type: text/plain\r\n")
    search_list = "anno_lemur/ebola/elasticsearch/search_list"
    f = open(search_list)
    lines = [line.strip() for line in f]
    try:
	index = lines.index(docno)
        if signal == "p" and index-1>=0:
	    print(lines[index-1])
	elif signal == "n" and len(lines)>index+1:
	    print(lines[index+1])
	else:
	    print("-1")
    except:
	print("-1")






form = cgi.FieldStorage()
moveHandle(form, environ)

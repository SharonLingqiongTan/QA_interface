import datetime
import json

# ?? all try except necessary ??


def writeLog(username, logline, signal=0):
    if signal == 1:
        path = '../../../userlog/'
    else:
        path = './userlog/'

    try:
        logh = open(path + '%s.log'%username,'a')
        logh.write(logline)
        logh.close()
    except: 
        pass

def log_login(username):
    logline = 'login  |  time: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"))
    writeLog(username, logline)

def log_logout(username):
    logline = 'logout  |  time: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"))
    writeLog(username, logline)

def log_mood(username, mood, topic_id, source, reason):
    logline = 'mood/%s |  time: %s  |  # of fields: 3  |  topic_id: %s  |  listsource: %s  |  message_name: %s\r\n\r\n'%(mood, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, source, reason.replace('\n',' '))
    writeLog(username, logline)

def log_domain(username, domain_id, domain_name):
    logline = 'domain/select  |  time: %s  |  # of fields: 2  |  domain_id: %s  |  domain_name: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), domain_id, domain_name)
    writeLog(username, logline)
        
def log_select_topic(username, topic_id, topic_name):
    logline = 'topic/select  |  time: %s  |  # of fields: 2  |  topic_id: %s  |  topic_name: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, topic_name.replace('\n',' '))
    writeLog(username, logline)

def log_edit_topic(username, domain_id, domain_name, topic_id, topic_name):
    logline = 'topic/edit  |  time: %s  |  # of fields: 4  |  domain_id: %s  |  domain_name: %s  |  topic_id: %s  |  newtopic_name:  %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), domain_id, domain_name, topic_id, topic_name.replace('\n',' '))
    writeLog(username, logline)

def log_add_topic(username, domain_id, domain_name, topic_id, topic_name):
    logline = 'topic/create  |  time: %s  |  # of fields: 4  |  domain_id: %s  |  domain_name: %s  |  topic_id: %s  |  topic_name:  %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), domain_id, domain_name, topic_id, topic_name.replace('\n',' '))
    writeLog(username, logline)

def log_delete_topic(username, domain_id, topic_id):
    logline = 'topic/delete  |  time: %s  |  # of fields: 2  |  domain_id: %s  |  topic_id: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), domain_id, topic_id)
    writeLog(username, logline)

def log_query(username, source, topic_id, topic_name, query):
    logline = 'query/%s  |  time: %s  |  # of fields: 3  |  topic_id: %s  |  topic_name: %s  |  query: %s\r\n\r\n'%(source, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"),  topic_id, topic_name.replace('\n',' '), query)
    writeLog(username, logline)

def log_findmore(username, color, topic_id, subtopic_id, subtopic_name):
    logline = 'findmore/%s  |  time: %s  |  # of fields: 3  |  topic_id: %s  |  subtopic_id: %s  |  subtopic_name: %s\r\n\r\n'%(color, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, subtopic_id, subtopic_name.replace('\n',' '))
    writeLog(username, logline)    

# def log_solr(username, domain_id, domain_name, topic_id, topic_name, query):
#     logline = 'solr/query  |  time: %s  |  # of fields: 5  |  domain_id: %s  |  domain_name: %s  |  topic_id: %s  |  topic_name: %s  |  query: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), domain_id, domain_name, topic_id, topic_name, query)
#     writeLog(username, logline)

# def log_terrier(username, domain_id, domain_name, topic_id, topic_name, query):
#     logline = 'terrier/query  |  time: %s  |  # of fields: 5  |  domain_id: %s  |  domain_name: %s  |  topic_id: %s  |  topic_name: %s  |  query: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), domain_id, domain_name, topic_id, topic_name, query)
#     writeLog(username, logline)

def log_show_hide_tagged(username, action, topic_id, topic_name):
    logline = 'tagged/%s  |  time: %s  |  # of fields: 2  |  topic_id: %s  |  topic_name: %s\r\n\r\n'%(action, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"),  topic_id, topic_name.replace('\n',' '))
    writeLog(username, logline)

def log_click_into_doc(username, topic_id, docno, source):
    logline = 'list/click  |  time: %s  |  # of fields: 4  |  topic_id: %s  |  docno: %s  |  listsource: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, docno, source)
    writeLog(username, logline)

def log_prev_doc(username, topic_id, docno):
    logline = 'doc/prev  |  time: %s  |  # of fields: 2  |  topic_id: %s  |  docno: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, docno)
    writeLog(username, logline)

def log_next_doc(username, topic_id, docno):
    logline = 'doc/next  |  time: %s  |  # of fields: 2  |  topic_id: %s  |  docno: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, docno)
    writeLog(username, logline)

def log_discard_doc(username, reason, topic_id, docno):
    logline = 'doc/%s  |  time: %s  |  # of fields: 2  |  topic_id: %s  |  docno: %s\r\n\r\n'%(reason, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, docno)
    writeLog(username, logline)

def log_goback_to_list(username, topic_id, docno, source):
    logline = 'list/go back  |  time: %s  |  # of fields: 3  |  topic_id: %s  |  docno: %s  |  listsource: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, docno, source)
    writeLog(username, logline)

def log_view_tagged_discarded_doc(username, origin, topic_id):
    logline = '%s/view  |  time: %s  |  # of  fields: 1  |  topic_id: %s\r\n\r\n'%(origin, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id)
    writeLog(username, logline)

def log_putback(username, origin, topic_id, docno):
    logline = '%s/put back  |  time: %s  |  # of  fields: 2  |  topic_id: %s  |  docno: %s\r\n\r\n'%(origin, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, docno)
    writeLog(username, logline)

def log_move_between_pages(): # ??
    pass

def log_add_subtopic(username, topic_id, topic_name, subtopic_id, subtopic_name):
    logline = 'subtopic/create  |  time: %s  |  # of fields: 4  |  topic_id: %s  |  topic_name: %s  |  subtopic_id: %s  |  subtopic_name: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, (topic_name.replace('|',' ')).replace('\n',' '), subtopic_id, subtopic_name.replace('\n',' '))
    writeLog(username, logline)

def log_edit_subtopic(username, topic_id, topic_name, subtopic_id, subtopic_name):
    logline = 'subtopic/edit  |  time: %s  |  # of fields: 4  |  topic_id: %s  |  topic_name: %s  |  subtopic_id: %s  |  newsubtopic_name: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), topic_id, (topic_name.replace('|',' ')).replace('\n',' '), subtopic_id, subtopic_name.replace('\n',' '))
    writeLog(username, logline)

def log_delete_subtopic(username, subtopic_id):
    logline = 'subtopic/delete  |  time: %s  |  # of fields: 1  |  subtopic_id: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), subtopic_id)
    writeLog(username, logline)

def log_add_passage(username, topic_id, topic_name, subtopic_id, subtopic_name, passage_id, passage_name, docno):
    logline = 'passage/create  |  time: %s  |  # of fields: 7  |  topic_id: %s  |  topic_name: %s  |  subtopic_id: %s  |  subtopic_name: %s  |  docno: %s  |  passage_id: %s  |  passage_name:  %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f").encode('UTF-8'), str(topic_id).encode('UTF-8'), ((topic_name.replace('|',' ')).replace('\n',' ')).encode('UTF-8') , str(subtopic_id).encode('UTF-8'), ((subtopic_name.replace('|',' ')).replace('\n',' ')).encode('UTF-8'), docno.encode('UTF-8'), str(passage_id).encode('UTF-8'), ((passage_name.decode('UTF-8')).encode('UTF-8')).replace('\n',' '))
    writeLog(username, logline)

def log_delete_passage(username, signal, passage_id, passage_name):
    if signal == '2':
        logline = 'passage/irrelevant |  time: %s  |  # of fields: 2  |  passage_id: %s |  passage_name: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), passage_id, passage_name.encode('UTF-8').replace('|',' ').replace('\n',' '))
    else:
        logline = 'passage/duplicate |  time: %s  |  # of fields: 2  |  passage_id: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), passage_id)
    writeLog(username, logline)

def log_grade_passage(username, passage_id, score):
    logline = "passage/grade  |  time: %s  |  # of fields: 2  |  passage_id: %s  |  score: %s\r\n\r\n"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %f"), passage_id, score)
    writeLog(username, logline)

def log_replace_passage(username, passage_id, subtopic_id):
    logline = "passage/move  |  time: %s  |  # of fields: 2  |  passage_id: %s  |  to subtopic_id: %s\r\n\r\n"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), passage_id, subtopic_id)
    writeLog(username, logline)

def log_highlight(username, topic_id, docno, hstring):
    logline = "highlight  |  time: %s  |  # of fields: 3  |  topic_id: %s  |  docno: %s  |  highlight_string: %s\r\n\r\n"%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), topic_id, docno, hstring)
    writeLog(username, logline)

def log_list(username, docs, result_size, num_tagged):
    logline = "result_size: %d  |  num_tagged:  %d\r\n"%(result_size, num_tagged)
    for doc, in docs:
        logline += doc + '\r\n'
    logline += '\r\n'
    writeLog(username, logline)

def log_finish(username, topic_id):
    logline = 'others/write_statement  |  time: %s  |  topic_id: %s\r\n\r\n'%(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), topic_id)
    writeLog(username, logline)
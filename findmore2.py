import requests
import sys
import database
from config import db_path
import mylog
from database import DBHandler

nistURL = "https://ir.nist.gov/dynamicdomain/moreLikeThis.php?"

def getDocList1():
    topic_id, subtopic_id = int(sys.argv[1]), int(sys.argv[2])
    atn_db = DBHandler('../../../database/test.db')

    atn_db.cur.execute('SELECT userid, domain_id, topic_name FROM topic WHERE topic_id=?', [topic_id])
    userid, domain_id, topic_name = atn_db.cur.fetchone()

    atn_db.cur.execute('SELECT username FROM user WHERE userid=?', [userid])
    username, = atn_db.cur.fetchone()

    atn_db.cur.execute('SELECT subtopic_name FROM subtopic WHERE subtopic_id=?', [subtopic_id])
    subtopic_name, = atn_db.cur.fetchone()

    corpus = ['EBOLA','POLAR','WEAPON'][domain_id-1]
    r = requests.get(nistURL + "CMD=UID=%d TID=%d STID=%d.%d CO=%s CMD=MORE_LIKE_THIS DATA=-"%(userid, topic_id, topic_id, subtopic_id, corpus), verify=False)

    #mylog.log_nist_findmore(username, sys.argv[1], topic_name, sys.argv[2], subtopic_name+"::"+r.url+"::")

    docs = r.content.split('\n')
    for doc in docs:
        if doc:
            print doc.split()[0]

def getDocList2():
    print "ebola-4955b0399813f904831aa974eb84e486c716d58fd5968a352a22fc0f62757203"
    print "ebola-363147f874472caff4e20681c3f50ff7652a00d6d94e78e5e65dc8ace760ebfc"
    print '11111'
    print 'eeeeee'
    print "ebola-3b78191de8b6c6f4473d3d9930fbcd35589d8ba07e3badaccb427a48a9f1ab20"
    print "ebola-0f817f9da047f85685886f8cd8aa3b63b0ab8caeaa206a556a8ad491b2e21b15"
    print "ebola-293d9564803185d09cbec3a4e8ff14d01859b0fdbe7c9f78e8f9df77600984ad"
getDocList1()
#getDocList2()

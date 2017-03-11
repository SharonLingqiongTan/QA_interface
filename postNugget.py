import requests
import md5

nistURL = "https://ir.nist.gov/dynamicdomain/moreLikeThis.php?CMD="

def sendRequest(packedString):
    m = md5.new()
    m.update(packedString)
    r = requests.get(nistURL+packedString, verify=False)
    return (m.hexdigest(), r.content)

def postNugget(userid, topic_id, subtopic_id, corpus, passage_id, docno, passage_name):
    packedString = "UID=%d TID=%d STID=%d.%d CO=%s CMD=NUGGET DATA=%d.%d.%d %s %s" % \
                    (userid, topic_id, topic_id, subtopic_id, corpus, topic_id, subtopic_id, passage_id, docno, passage_name)
    return sendRequest(packedString)

def gradeNugget(userid, topic_id, subtopic_id, corpus, passage_id, score):
    packedString = "UID=%d TID=%d STID=%d.%d CO=%s CMD=NUGGET DATA=%d.%d.%d ADD_GRADE %s" % \
                    (userid, topic_id, topic_id, subtopic_id, corpus, topic_id, subtopic_id, passage_id, score)
    return sendRequest(packedString)

def deleteNugget(userid, topic_id, subtopic_id, corpus, passage_id, reason):
    packedString = "UID=%d TID=%d STID=%d.%d CO=%s CMD=NUGGET DATA=%d.%d.%d DELETE %s" % \
                    (userid, topic_id, topic_id, subtopic_id, corpus, topic_id, subtopic_id, passage_id, reason)
    return sendRequest(packedString)

def discardDoc(userid, topic_id, corpus, CMD, docno): # CMD = IRRELEVANT OR DUPLICATE
    packedString = "UID=%d TID=%d STID=- CO=%s CMD=%s DATA=%s" % \
                    (userid, topic_id, corpus, CMD, docno)
    return sendRequest(packedString)

#postNugget(10,10,1,'EBOLA', 1, "ebola-87ff6bfd00371c432757c1136b7ecc5bb502dd0008569fd8e1e2593a4b851ce4", "Genetic and epidemiological evidence from WHO officially confirms that the outbreak of Ebola Virus Disease in the Democratic Republic of Congo is unrelated ...http://www.forbes.com/sites/davidkroll/2014/09/02/ebola-outbreaks-unrelated-in-west-africa-and-democratic-republic-of-congo/")
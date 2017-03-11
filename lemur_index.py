# -*- coding: utf-8 -*-
import json,sys
reload(sys)
sys.setdefaultencoding("utf-8")
input_path = "/data2/home/jw1498/built_elasticsearch_index"
feature_list = ["name", "age", "location", "phone", "email", "ethnicity", "height", "weight", "hair_color", "eye_color"]
for i in range(1, 7):
    input_file_path = input_path + "/" + str(i) + "_index"
    output_path = "/data2/home/jw1498/corpus/" + str(i)
    with open(input_file_path) as f:
    	with open(output_path,"w") as o:
            for line in f:
            	doc = json.loads(line)
            	o.write("<DOC>\n")
            	o.write("<DOCNO>"+doc["_id"]+"</DOCNO>\n")
            	o.write("<HTML>\n")
            	o.write("<BODY>\n")
                for feature in feature_list:
		    if doc[feature]:
		        o.write("<" + feature + ">" + feature + ": " + str(doc[feature]) + "</" + feature + ">" + "\n")
		    else:
		        o.write("<" + feature + ">" + feature + ": " + "NULL" + "</" + feature + ">" + "\n") 
                url = doc["url"]
                o.write("<url>"+url+"</url>\n")
                o.write("<raw_content>"+doc["raw_content"]+"</raw_content>\n")
                o.write("</BODY>\n")
                o.write("</HTML>\n")
                o.write("</DOC>\n")

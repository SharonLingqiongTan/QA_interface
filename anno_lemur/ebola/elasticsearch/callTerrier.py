import sys
sys.path.insert(0,"/data2/apps/anaconda2/lib/python2.7/site-packages")
import certifi,os,yaml,re,json
from fuzzywuzzy import fuzz
from elasticsearch import Elasticsearch,RequestsHttpConnection


with open("structureQuerylog") as f:
	q = open("search_list","w")
	lines = f.readlines()
	if lines:
		query = lines[-1].strip()
		must_list = []
		should_list = []
		query_body = {"size":500,"query":{"bool":{"must":[{"match":{"raw_content": ""}}],"should":[]}} }
		query_dic = {}
		if query.endswith(";"):
			age_min = 0
			age_max = 0
			height_min = 0
			height_max = 0
			query_terms = query[:-1].split(";")
			query_dic = {x.split(":")[0]:x.split(":")[1] for x in query_terms}
			feature_should_search_map = {"name":"name","hairColor":"hair","eyeColor":"eye","nationality":"nationality","ethnicity":"ethnicity","reviewSite":"review","reviewSiteId":"review","email":"email","phone":"phone","state":"","city":"","price":"","multiple_providers":"","socialMedia":"","socialMediaId":"","services":"","height":"height","weight":"weight","post_date":"posted"}
			for key in query_dic:
				if key == "phone":
					phone = re.sub("\D","",query_dic[key])
					must_list.append(phone[:3])
					must_list.append(phone[3:6])
					must_list.append(phone[6:])
					should_list.append("("+phone[:3]+")"+phone[3:6]+"-"+phone[6:])
					should_list.append(phone[:3]+"-"+phone[3:6]+"-"+phone[6:])
					should_list.append("phone")
				elif key == "age" or key == "height":
					pass
				#elif key == "ethnicity":
				#	pass
				else:
					must_list.append(query_dic[key])
					must_list.append(key)
			if "age" in query_dic:
				age_min = int(query_dic["age"][:2])
				age_max = int(query_dic["age"][2:])
				should_list.append("age")
			if "height" in query_dic:
				height_min = int(query_dic["height"][:3])
				height_max = int(query_dic["height"][3:])
				should_list.append("height")
			if must_list:
			    query_body["query"]["bool"]["must"][0]["match"]["raw_content"] = " AND ".join(must_list)
			else:
			    query_str = ""
			    if "age" in query_dic:
				query_str += "age"
			    if "height" in query_dic:
				query_str += "height"
			    query_body["query"]["bool"]["must"][0]["match"]["raw_content"] = query_str
			should_arr = []
			for word in should_list:
				dic = {}
				dic["match"] = {}
				dic["match"]["raw_content"] = word
				should_arr.append(dic)
			query_body["query"]["bool"]["should"] = should_arr
			if "age" in query_dic:
				query_body["query"]["bool"]["must"].append({"range" : {"age" : {"gte" : age_min,"lte" : age_max}}})
			if "height" in query_dic:
				query_body["query"]["bool"]["must"].append({"range" : {"height" : {"gte" : height_min,"lte" : height_max}}})
		else:
			query_body["query"]["bool"]["must"][0]["match"]["raw_content"] = query
		es = Elasticsearch(["localhost:9200/positiongt"],request_timeout=60)
		response = es.search(body=query_body,request_timeout=60)
		documents = response["hits"]["hits"]
		if "ethnicity" in query_dic:
			for document in documents:
				if "ethnicity" in document["_source"] and document["_source"]["ethnicity"]:
					ethnicities = map(lambda x:x.lower(),document["_source"]["ethnicity"])
					#print(ethnicities)
					if query_dic["ethnicity"] in ethnicities:
						print(document["_id"])
						q.write(document["_id"])
						q.write("\n")
					else:
						f = open("nation_continent.txt")
						ethnicity_dic = yaml.load(f)
						candidate_countries = ethnicity_dic[query_dic["ethnicity"]]
						for eth_candi in ethnicities:
							for coun_candi in candidate_countries:
								if fuzz.ratio(eth_candi,coun_candi.lower())>=80:
									print(document["_id"])
									q.write(document["_id"])
                                                			q.write("\n")
									break

		else:
			for document in documents:
				q.write(document["_id"])
                                q.write("\n")
				print document["_id"]



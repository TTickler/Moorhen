#!/usr/bin/python

import json
import sys
import os
import ConfigParser
import elasticsearch

def main(argv):

    #try:
    es = elasticsearch.Elasticsearch('http://localhost:9200')
    
    stat_holder = {"1": 0, "2": 0, "3": 0, "4": 0}

    for arg in argv:
        stat_holder[str(es_query(arg, es))] += 1

    print(status_check(stat_holder))
    sys.exit()
    #except:
	#sys.exit()


def status_check(stat_holder):
    
    if stat_holder["4"] != 0:
        status = 4
    elif stat_holder["4"] == 0 and stat_holder["3"] != 0:
        status = 3
    else:
        status = 2

    return status


def es_query(arg, es):
    
    esQuery = {
         "query": {
            "match": {"hostname": arg}
                   },
             "size": "1",
             "sort": [
                      {
                        "@timestamp": {
                         "order": "desc"
                                      }
                       }
                     ]
              }

    query_results = es.search(index="test3", doc_type="sys_health", body=json.dumps(esQuery))

    #print query_results

    return query_results["hits"]["hits"][0]["_source"]["System"]


if __name__ == "__main__":


    main(sys.argv[1:])



import elasticsearch 
from datetime import datetime
import sys
import json

class elasticsearchClient(object):
    def __init__(self, host, port=9200, timeout=10, client_cert='', client_key='', maxsize=5):

        #Elasticsearch connection parameters
        self._host = host
	print(self._host)
	self._port = port
        self._timeout = timeout
        self._client_cert = client_cert
        self._client_key = client_key
        self._max_size = maxsize
	self._elasticsearchInstance = self.clientCreation()


    @property
    def instance(self):
	return self._elasticsearchInstance

    @instance.setter
    def instance(self, elasticsearch_instance):
	self._elasticsearchInstance = instance

    #tries to create elasticsearch client. Returns true if client is successfully created
    #else, returns false
    def clientCreation(self):
	
	#try/except not provided here as a failure of client creation indicates a failure of another component
	#and should be sorted until Server/ modules continue operation	
	elasticsearchInstance = elasticsearch.Elasticsearch([{'host': self._host, 'port': self._port}])

	return elasticsearchInstance
       

class Query(elasticsearchClient):
	def __init__(self, host, port=9200, timeout=10, client_cert='', client_key='', maxsize=5):
		elasticsearchClient.__init__(self, host, port, timeout, client_cert, client_key, maxsize)


	def queryES(self, index, doc_type, query_body):
	#	try:		
		query_results = self.instance.search(index=index, doc_type=doc_type, body=json.dumps(query_body))
		print(query_results)
	#	except:
	#		print("Failed to get results from querying elasticsearch. Exiting application. Check if elasticsearch cluster is running or if configuration is valid.")
	#		sys.exit()
		return query_results



class Index(elasticsearchClient):
	def __init__(self, host, port=9200, timeout=10, client_cert='', client_key='', maxsize=5):
		elasticsearchClient.__init__(self, host, port, timeout,client_cert, client_key, maxsize)

        def putInto(self,index, doc_type ,body):

		try:
                	response = elasticsearch.index(index=index, doc_type=doc_type, body=body)
		except:
			print("Failed to index element.")

		return response


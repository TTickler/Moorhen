import elasticsearch 
from datetime import datetime

class elasticsearchClient(object):
    def __init__(self, host, port, timeout=10, client_cert='', client_key='', maxsize=5):

        #Elasticsearch connection parameters
        self._host = host
        self._port = port
        self._timeout = timeout
        self._client_cert = client_cert
        self._client_key = client_key
        self._max_size = maxsize
	self.es = ''

	#attempts to initialize a client 
	self.clientCreation()

    #tries to create elasticsearch client. Returns true if client is successfully created
    #else, returns false
    def clientCreation(self):
	
	try:
		self.es = elasticsearch.Elasticsearch(self._host + ':' + str(self._port))
		return True

	except:
		print("Failed to connect to elasticsearch.")
		return False
       

class Query(elasticsearchClient):
	def __init__(self, host, port, timeout=10, client_cert='', client_key='', maxsize=5):
		elasticsearchClient.__init__(host, port, timeout, client_cert, client_key, maxsize)


	def queryES(self, index, doc_type, query_body):
		try:		
			query_results = elasticsearchClient.es.search(index=index, doc_type=doc_type, body=query_body)

		except:
			print("Failed to get results from querying elasticsearch")
		return query_results



class Index(elasticsearchClient):
	def __init__(self):
		elasticsearchClient.__init__(host,port,timeout,client_cert, client_key, maxsize)

        def putInto(self,index, doc_type ,body):

		try:
                	response = elasticsearch.index(index=index, doc_type=doc_type, body=body)
		except:
			print("Failed to index element.")

		return response

import elasticsearch5 #elasticsearch5 is used for clarity and stability due to ELK stack being 5.x.x
from datetime import datetime

class elasticsearchClient(object):
    def __init__(self, host, port, timeout=10, client_cert='', client_key='', maxsize=5):

        #instantiation of elasticsearch5 object
        self.es = elasticsearch5

        #
        self._connection_type = ''
        self._


        #Elasticsearch connection parameters
        self._host = host
        self._port = port
        self._timeout = timeout
        self._client_cert = client_cert
        self._client_key = client_key
        self._max_size = maxsize


    def connect(self):

        #encapsulation of transport related to logic
        self.transport = self.es.Transport()

        #
        self.connection = self.es.Connection()


class Query(elasticsearchClient):
	def __init__(self, host, port, timeout=10, client_cert='', client_key='', maxsize=5):
		delasticsearchClient.__init__(host, port, timeout, client_cert, client_key, maxsize)


	def queryES(self, index, doc_type, query_body):
		
		query_results =
		return query_results





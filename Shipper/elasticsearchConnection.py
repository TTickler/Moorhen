import elasticsearch5 #elasticsearch5 is used for clarity and stability due to ELK stack being 5.x.x
from datetime import datetime

class elasticsearchConnection(object):
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
        self.connect.


#Elasticsearch connection using urllib3 library and http protocol
class EShttpConnection(elasticsearchConnection):
    def __init__(self, host, port, timeout=10, client_cert='', client_key='', maxsize=5):
        elasticsearchConnection.__init__()





#Elasticsearch connection using requests library
class ESUrllib3Connection(elasticsearchConnection):
    def __init__(self, host, port, timeout=10, client_cert='', client_key='', maxsize=5):
        elasticsearchConnection.__init__()








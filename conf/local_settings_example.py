from django.core.cache import cache
from elasticsearch import Elasticsearch
from urllib3 import Timeout


##### Change config below
cache.set('ES_HOST',"<your ES instance path>")
cache.set('ES_PORT',<ES instance port goes here>)

# this helps in getting the fieldnames to be displayed in grafana
cache.set('DOC_TYPE',"<whats the doc type you're gonna look at>")

# recommended: to search faster, your ES data should be named in
# this format <prefix>-xyz. ES is not graphite, simply said.
# hence we need to take care of a few things. data is ingested
# in an entirely different manner.
cache.set('INDEX_PREFIX',"<your index prefix>")

# this one is the starting metric1 in the graphite like path as below:
# metric1.path1.path2 .. there has to be a starting point, right?
cache.set('FIELD',"<the fieldname to be displayed in dropdown list>")

# this is so that fresh mapping is rendered
cache.set('FRESH',<boolean: True/False>)

# set the hostname where the application is hosted, this is to take care
# of debug mode in django
import socket as _sock
cache.set('HOSTNAME',_sock.gethostname())
del _sock

# Initiate ElasticSearch connection
timeoutobj = Timeout(total=1200, connect=10, read=600)
ES = Elasticsearch(host=cache.get('ES_HOST'), port=cache.get('ES_PORT'),
                   timeout=timeoutobj, max_retries=0)

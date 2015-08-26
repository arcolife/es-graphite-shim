import os
from django.core.cache import cache

# don't change this. It's not present in main settings.py file, because
# we needed it here first for the _indices_path and _fields_path
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# change this to wherever you wish them to exist.
cache.set('_indices_path', os.path.join(BASE_DIR, \
						'egs/lib/mappings/open_indices.json'))
cache.set('_fields_path', os.path.join(BASE_DIR, \
						'egs/lib/mappings/fields_list.json'))

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

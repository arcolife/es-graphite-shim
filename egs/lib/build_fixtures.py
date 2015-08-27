"""
get the data to be displayed in drop down list in grafana
"""

import json
import logging
import os, sys
from time import ctime
from django.conf import settings
from threading import Thread, Event
from django.core.cache import cache
from lib.get_es_metadata import get_mappings as _get_mappings
from lib.get_es_metadata import get_fieldnames as _get_fieldnames
from lib.get_es_metadata import get_open_indices_list as \
    _get_open_indices_list


_run = True
_index = Event()

_indices_path = os.path.join(settings.BASE_DIR, \
                             'lib/mappings/open_indices.json')
_fields_path = os.path.join(settings.BASE_DIR, \
                            'lib/mappings/fields_list.json')

logger = logging.getLogger(__name__)


def build_open_indices(_new=None):
    ''' 
    query list of indices in state:open
    '''
    global _run, _index
    while _run:
        _index.wait()
        # Clear before we perform all the indexing steps so that if another
        # upload or signal comes in after we wake up, we'll loop around again
        # to service that request.
        _index.clear()
        
        if _run:
            try:
                logger.info("[%s] _bkgthd._fixture_builder - begin (%s)" \
                            % (ctime(), 'build_open_indices'))
                
                # collect info on open indices
                if _new:
                    logger.info("[%s] _bkgthd._fixture_builder - [open indices] building new list" \
                                % (ctime()))
                    _OPEN_INDICES = _get_open_indices_list(settings.ES, \
                                                           cache.get('INDEX_PREFIX'), \
                                                           cache.get('DOC_TYPE'))
                    # dict with index name as key and fieldnames as values
                    f = open(_indices_path, 'wb')
                    f.write(bytes(json.dumps(_OPEN_INDICES), 'UTF-8'))
                    f.close()    
                else:
                    logger.info("[%s] _bkgthd._fixture_builder - [open indices] opening saved list" \
                                % (ctime()))
                    f = open(_indices_path, 'rb')
                    _OPEN_INDICES = json.loads(f.read().decode('UTF-8'))
                    f.close()

                cache.set('_OPEN_INDICES', _OPEN_INDICES)
                logger.info("[%s] _bkgthd._fixture_builder - len([open indices]) = %d" \
                            % (ctime(), len(_OPEN_INDICES)))

                # collect info on fieldnames (for dropdown list display)
                logger.info("[%s] _bkgthd._fixture_builder - [fieldnames] building new list" \
                            % (ctime()))

                # dict with index name as key and fieldnames as values
                _FIELDS = _get_fieldnames(settings.ES, \
                                          cache.get('FIELD'), \
                                          cache.get('_OPEN_INDICES'), \
                                          doc_type=cache.get('DOC_TYPE'))

                f = open(_fields_path, 'wb')
                f.write(bytes(json.dumps(_FIELDS), 'UTF-8'))
                f.close()
                cache.set('_FIELDS', _FIELDS)

                # get mappings
                logger.info("[%s] _bkgthd._fixture_builder - [mappings] getting mappings" \
                            % (ctime()))
                
                cache.set('_MAPPINGS', _get_mappings(settings.ES, cache.get('DOC_TYPE'), \
                                                     _fresh=cache.get('FRESH')))
                
            except Exception as exc:
                logger.info("[%s] _bkgthd._fixture_builder - err (%s): %r" % \
                            (ctime(), 'build_open_indices', exc), file=sys.stderr)
            else:
                logger.info("[%s] _bkgthd._fixture_builder - end (%s)" % \
                            (ctime(), 'build_open_indices'))
        else:
            logger.info("[%s] _bkgthd._fixture_builder: no-op" \
                        % ctime(), file=sys.stderr)

            
def start_threading():
    _index.set()

    if not os.path.exists(_indices_path) or \
       not os.path.getsize(_indices_path):
        # set _new to True
        _form_new = True
    else:
        # set _new to False
        _form_new = False

    _bkgthd = Thread(target=build_open_indices, daemon=True, kwargs={'_new': _form_new})
    _bkgthd.start()

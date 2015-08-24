"""
get the data to be displayed in drop down list in grafana
"""

import json
import os, sys
from time import ctime
from threading import Thread, Event
from django.core.cache import cache
from lib.get_es_metadata import get_mappings as _get_mappings
from lib.get_es_metadata import get_fieldnames as _get_fieldnames
from lib.get_es_metadata import get_open_indices_list as \
                                        _get_open_indices_list
from django.conf import settings

_run = True
_index = Event()


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
                print("[%s] _bkgthd._fixture_builder - begin (%s)" % (ctime(), 'build_open_indices'))
                if _new:
                    print("[%s] _bkgthd._fixture_builder - [open indices] building new list" % (ctime()))
                    _OPEN_INDICES = _get_open_indices_list(settings.ES, \
                                                        cache.get('INDEX_PREFIX'), \
                                                        cache.get('DOC_TYPE'))
                    # dict with index name as key and fieldnames as values
                    f = open(cache.get('_indices_path'), 'wb')
                    f.write(bytes(json.dumps(_OPEN_INDICES), 'UTF-8'))
                    f.close()    
                else:
                    print("[%s] _bkgthd._fixture_builder - [open indices] opening saved list" % (ctime()))
                    f = open(cache.get('_indices_path'), 'rb')
                    _OPEN_INDICES = json.loads(f.read().decode('UTF-8'))
                    f.close()

                cache.set('_OPEN_INDICES', _OPEN_INDICES)
                print("[%s] _bkgthd._fixture_builder - len([open indices]) = %d" % (ctime(), len(_OPEN_INDICES)))

                # get fieldnames list
                if not os.path.exists(cache.get('_fields_path')):
                    print("[%s] _bkgthd._fixture_builder - [fieldnames] building new list" % (ctime()))
                    _FIELDS = _get_fieldnames(settings.ES, \
                                            cache.get('FIELD'), \
                                            cache.get('_OPEN_INDICES'), \
                                            doc_type=cache.get('DOC_TYPE'))
                else:
                    print("[%s] _bkgthd._fixture_builder - [fieldnames] opening saved list" % (ctime()))
                    # dict with index name as key and fieldnames as values
                    f = open(cache.get('_fields_path'), 'wb')
                    f.write(bytes(json.dumps(_FIELDS), 'UTF-8'))
                    f.close()
                cache.set('_FIELDS', _FIELDS)

                print("[%s] _bkgthd._fixture_builder - [mappings] getting mappings" % (ctime()))
                cache.set('_MAPPINGS', _get_mappings(settings.ES, cache.get('DOC_TYPE'), _fresh=cache.get('FRESH')))
                print("[%s] _bkgthd._fixture_builder - [mappings] got mappings" % (ctime()))

            except Exception as exc:
                print("[%s] _bkgthd._fixture_builder - err (%s): %r" % (ctime(), 'build_open_indices', exc), file=sys.stderr)
            else:
                print("[%s] _bkgthd._fixture_builder - end (%s)" % (ctime(), 'build_open_indices'))
        else:
            print("[%s] _bkgthd._fixture_builder: no-op" % ctime(), file=sys.stderr)


def main():
    """
    start threading
    """
    _index.set()
    # pool = eventlet.GreenPool()
    # process indices/fieldname list
    if not os.path.exists(cache.get('_indices_path')) or not os.path.getsize(cache.get('_indices_path')):
        #gevent.spawn(build_open_indices(_new=True))
        # pool.spawn_n(build_open_indices(_new=True))
        _bkgthd = Thread(target=build_open_indices, daemon=True, kwargs={'_new': True})
    else:
        #gevent.spawn(build_open_indices(_new=False))
        # pool.spawn_n(build_open_indices(_new=False))
        _bkgthd = Thread(target=build_open_indices, daemon=True, kwargs={'_new': False})
    _bkgthd.start()

    # _bkgthd2 = Thread(target=_get_mappings, daemon=True, args=(ES, DOC_TYPE),  kwargs={'_fresh' : FRESH})
    # _bkgthd2.start()

    # for body in pool.imap(foo): print(body)
    # # remove methods which won't be used any longer
    # del _get_fieldnames
    # del _get_open_indices_list
    # # build an aggregate dict of mappings to be referred 
    # # for field validation each time a query is issued
    # del _get_mappings
    # del json

'''
This is for loading stubs for testing
'''

import json

query = 'root_metric.doc_type.sub_metric_1.sub_metric_2'
metrics = { 'mappings' : {
    'root_metric' : { 
        'properties' : {
            'doc_type' : {
                'properties' : {
                    'sub_metric_1' : {
                        'properties' : {
                            'sub_metric_2' 
                        }
                    }
                }
            }
        }
    }
}}

try:
    f = open('./es_mappings_test.json','r')
    mappings = json.loads(f.read())
    f.close()
except:
    raise

sample_resp = { "leaf": 0,
                "context": {} ,
                "text": "sub_metric_2",
                "expandable": 1,
                "id": "root_metric.doc_type.sub_metric_1.sub_metric_2",
                "allowChildren": 1 
            }

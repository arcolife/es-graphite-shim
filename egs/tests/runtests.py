#!/usr/bin/env python3

"""
One could run tests directly through manage.py,
like this:
    $ python -Wall manage.py test --pattern="tests_*.py"
                            OR 
    $ python -Wall manage.py test tests.runtests.QueryFormatterTest"

where the flag -Wall is supplied as well, although it is optional 
but recommended, for tips on writing better code. (Warning Flags)
"""

import unittest
from egs import query_formatter
from tests import sample_inputs

class QueryFormatterTest(unittest.TestCase):
    '''
    Test the complete module responsible for 
    formatting the queries from API.
    '''        
    # def setUp(self):
    #     print('In setUp()')
    #     self.fixture = range(1, 10)

    # def tearDown(self):
    #     print('In tearDown()')
    #     del self.fixture

    def test_flatten_list(self):
        assert query_formatter.flatten_list([[1,2],[3]]) \
            == [1,2,3]

    def test_form_response(self):
        assert query_formatter.form_response(text="sub_metric_2",
                                             _id=sample_inputs.query) \
                                             == sample_inputs.sample_resp
        
    def test_iterate_mappings(self):
        res = query_formatter.iterate_mappings(query=sample_inputs.query, \
                                               metrics=sample_inputs.metrics)
        print(res)
        assert res == None
        # raise RuntimeError('Test error!')
        # self.assertTrue(True, "fail message")
        # self.failUnless(True)
        
    def test_find_metrics(self):
        self.assertTrue(True)
            
    def test_restructure_query(self):
        self.assertTrue(True)
            
    def test_query_es(self):
        self.assertTrue(True)
            
    def test_build_query(self):
        self.assertTrue(True)
       
    def test_render_metrics(self):
        self.assertTrue(True)            


if __name__ == '__main__':
    unittest.main()

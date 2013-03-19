from webtest import TestApp
import unittest

from organicseeds_webshop_api import main

class TestWebshopAPI(unittest.TestCase):

    def test_case(self):
        app = TestApp(main({}))
        import ipdb; ipdb.set_trace()
        app.post_json('/categories',
                      dict(categories=[
                           dict(foo="d", bar="bar", baz="baz"),
                           dict(foo="d", bar="bar", baz="baz"),
                           dict(foo="d", bar="bar", baz="baz"),
                           dict(foo="d", bar="bar", baz="baz"),
                           ]
                           ),

                      )

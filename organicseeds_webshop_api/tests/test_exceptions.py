import unittest


class TestExceptionsUnitTest(unittest.TestCase):

    def test_exceptions_500(self):
        from organicseeds_webshop_api import exceptions
        error = exceptions._500()
        assert error.status == "500 Internal Server Error"

    def test_exceptions_502(self):
        from organicseeds_webshop_api import exceptions
        error = exceptions._502(msgs=[("location", "name", "description")])
        assert error.status == "502 Bad Gateway"
        assert error.json_body == {u'status': u'errors', u'errors':
                                   [{u'description': u'description',
                                     u'name': u'name',
                                     u'location': u'location'}]}
        assert error.success == []
        assert error.errors == []

        error = exceptions._502(msgs=[("location", "name", "description")],
                                success=[1], errors=[("1", "wrong_method")])
        assert error.success == [1]
        assert error.errors == [("1", "wrong_method")]

    def test_exceptions_400(self):
        from organicseeds_webshop_api import exceptions
        error = exceptions._400(msgs=[("location", "name", "description")])
        assert error.status == '400 Bad Request'
        assert error.json_body == {u'status': u'errors', u'errors':
                                   [{u'description': u'description',
                                     u'name': u'name',
                                     u'location': u'location'}]}

import unittest
import json
import pytest
from pyramid import testing


class Test_Schemata_Validate_Identifier(unittest.TestCase):


    def test_valid_values(self):
        from organicseeds_webshop_api.schemata import Identifier
        import colander
        validator = Identifier.validator
        node = colander.SchemaNode(colander.String())
        assert(validator(node, u"111") == None)
        assert(validator(node, u"ddd") == None)
        assert(validator(node, u"11_ddd") == None)

    def test_invalid_values(self):
        from organicseeds_webshop_api.schemata import Identifier
        import colander
        from colander import Invalid
        validator = Identifier.validator
        node = colander.SchemaNode(colander.String())
        with pytest.raises(Invalid):
            validator(node, u"")
        with pytest.raises(Invalid):
            validator(node, u"d?")


class Test_Schemata_Validate_IntegerGtNull(unittest.TestCase):

    def test_valid_values(self):
        from organicseeds_webshop_api.schemata import IntegerGtNull
        import colander
        validator = IntegerGtNull.validator
        node = colander.SchemaNode(colander.Integer())
        assert(validator(node, 50000) == None)
        assert(validator(node, 1) == None)

    def test_invalid_values(self):
        from organicseeds_webshop_api.schemata import IntegerGtNull
        import colander
        validator = IntegerGtNull.validator
        node = colander.SchemaNode(colander.Integer())
        with pytest.raises(colander.Invalid):
            validator(node, 0)
        with pytest.raises(colander.Invalid):
            validator(node, -1)


class Test_Schemata_Validate_RelativeFilePathUnix(unittest.TestCase):

    def test_valid_values(self):
        from organicseeds_webshop_api.schemata import RelativeFilePathUnix
        import colander
        validator = RelativeFilePathUnix.validator
        node = colander.SchemaNode(colander.String())
        assert(validator(node, u"as-d_ffdg444ds..af") == None)
        assert(validator(node, u"./asdfdsaf/sdfdsaf") == None)
        assert(validator(node, u"asdfdsaf/dsafdsaf") == None)

    def test_invalid_values(self):
        from organicseeds_webshop_api.schemata import RelativeFilePathUnix
        import colander
        validator = RelativeFilePathUnix.validator
        node = colander.SchemaNode(colander.String())
        with pytest.raises(colander.Invalid):
            validator(node, u"")
        with pytest.raises(colander.Invalid):
            validator(node, u"/sdafdsaf")
        with pytest.raises(colander.Invalid):
            validator(node, u"http://www.x.org")


class Test_Schemata_Validate_IntegerGtEqNull(unittest.TestCase):

    def test_valid_values(self):
        from organicseeds_webshop_api.schemata import IntegerGtEqNull
        import colander
        validator = IntegerGtEqNull.validator
        node = colander.SchemaNode(colander.Integer())
        assert(validator(node, 50000) == None)
        assert(validator(node, 1) == None)
        assert(validator(node, 0) == None)

    def test_invalid_values(self):
        from organicseeds_webshop_api.schemata import IntegerGtEqNull
        import colander
        validator = IntegerGtEqNull.validator
        node = colander.SchemaNode(colander.Integer())
        with pytest.raises(colander.Invalid):
            validator(node, -1)

class Test_Schemata_Validate_references(unittest.TestCase):

     def test_validate_vpe_type_id_valid(self):
        from organicseeds_webshop_api.schemata import deferred_validate_vpe_type_id
        import colander
        validator = deferred_validate_vpe_type_id
        node = colander.SchemaNode(colander.String())
        request = testing.DummyRequest()
        request.body = json.dumps(
                       {"vpe_types": [{"id": "type1"},{"id": "type2"}],
                        "items": [{"vpe_type_id": "type1"}]
                       })
        kw = {"request": request}
        assert(validator(node, kw).choices == [u'type1', u'type2'])
        request.body = json.dumps(
                       {"vpe_types": [],
                        "items": [{"vpe_type_id": "type1"}]
                       })
        assert(validator(node, kw).choices == [])

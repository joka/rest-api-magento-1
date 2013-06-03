import unittest
import pytest


class Test_Schemata_Validate_Float(unittest.TestCase):

    def test_float_decimal_points_valid(self):
        from organicseeds_webshop_api.schemata import \
            float_decimal_points
        node = object()
        assert float_decimal_points(node, 1, 2) is None
        assert float_decimal_points(node, 1.1, 2) is None
        assert float_decimal_points(node, 1.11, 2) is None

    def test_float_decimal_points_invalid(self):
        from colander import Invalid
        from organicseeds_webshop_api.schemata import \
            float_decimal_points
        node = object()
        with pytest.raises(Invalid):
            float_decimal_points(node, 1.111, 2)

    def test_two_decimal_points_invalid(self):
        from colander import Invalid
        from organicseeds_webshop_api.schemata import \
            two_decimal_points
        node = object()
        with pytest.raises(Invalid):
            two_decimal_points(node, 1.111)

    def test_four_decimal_points_invalid(self):
        from colander import Invalid
        from organicseeds_webshop_api.schemata import \
            four_decimal_points
        node = object()
        with pytest.raises(Invalid):
            four_decimal_points(node, 1.11111)


class Test_Schemata_Validate_Identifier(unittest.TestCase):

    def test_valid_values(self):
        from organicseeds_webshop_api.schemata import Identifier
        import colander
        validator = Identifier.validator
        node = colander.SchemaNode(colander.String())
        assert(validator(node, u"111") is None)
        assert(validator(node, u"ddd") is None)
        assert(validator(node, u"11_ddd") is None)

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
        assert(validator(node, 50000) is None)
        assert(validator(node, 1) is None)

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
        assert(validator(node, u"as-d_ffdg444ds..af") is None)
        assert(validator(node, u"./asdfdsaf/sdfdsaf") is None)
        assert(validator(node, u"asdfdsaf/dsafdsaf") is None)

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
        assert(validator(node, 50000) is None)
        assert(validator(node, 1) is None)
        assert(validator(node, 0) is None)

    def test_invalid_values(self):
        from organicseeds_webshop_api.schemata import IntegerGtEqNull
        import colander
        validator = IntegerGtEqNull.validator
        node = colander.SchemaNode(colander.Integer())
        with pytest.raises(colander.Invalid):
            validator(node, -1)

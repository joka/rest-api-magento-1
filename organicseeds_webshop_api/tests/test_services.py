import unittest
import json
import yaml
import yaml2json
import pytest
import os.path
from webtest import TestApp
from webtest.app import AppError
from pyramid import testing


ITEMS_POST_EXAMPLE_YAML = "/testdata/items_post.yaml"


def yaml_to_json(yamlstring):
    yamldata = yaml.load(yamlstring)
    jsondata = yaml2json.convertArrays(yamldata)
    return jsondata


class TestServicesIntegration(unittest.TestCase):

    def setUp(self):
        import organicseeds_webshop_api
        self.request = testing.DummyRequest()
        self.request.context = testing.DummyResource()
        self.config = testing.setUp(request=self.request, settings = {"zodbconn.uri": "memory://"})
        self.config.include("pyramid_zodbconn")
        self.config.include(organicseeds_webshop_api.utilities)
        self.config.include(organicseeds_webshop_api.models)
        self.request.root = organicseeds_webshop_api.root_factory(self.request)
        testfilepath = os.path.join(organicseeds_webshop_api.tests.__path__[0] +  ITEMS_POST_EXAMPLE_YAML)
        self.items_post_testfile = open(testfilepath, "r")
        self.items_post_testdata = yaml.load(self.items_post_testfile)

    def tearDown(self):
        testing.tearDown()
        self.items_post_testfile.close()

    def test_items_post(self):
        from organicseeds_webshop_api.services import items_post
        jsonstr = json.dumps(self.items_post_testdata)
        self.request.body = jsonstr
        response =  items_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesFunctional(unittest.TestCase):

    def setUp(self):
        import organicseeds_webshop_api
        from organicseeds_webshop_api import main
        self.app = TestApp(main({"zodbconn.uri": "memory://"}))
        testfilepath = os.path.join(organicseeds_webshop_api.tests.__path__[0] +  ITEMS_POST_EXAMPLE_YAML)
        self.items_post_testfile = open(testfilepath, "r")
        self.items_post_testdata = yaml.load(self.items_post_testfile)

    def tearDown(self):
        self.items_post_testfile.close()


    #def test_categories_put(self):
        #jsondata = self.items_post_testdata
        #self.app.post_json('/categories', jsondata)

    def test_items_put(self):
        jsondata = self.items_post_testdata
        resp = self.app.post_json('/items', jsondata)
        assert resp.status_int == 200


class Test_Schemata_Validate_Identifier(unittest.TestCase):


    def test_valid_values(self):
        from organicseeds_webshop_api.schemata import validate_identifier
        import colander
        validator = validate_identifier
        node = colander.SchemaNode(colander.String())
        assert(validator(node, u"111") == None)
        assert(validator(node, u"ddd") == None)
        assert(validator(node, u"11_ddd") == None)

    def test_invalid_values(self):
        from organicseeds_webshop_api.schemata import validate_identifier
        import colander
        from colander import Invalid
        validator = validate_identifier
        node = colander.SchemaNode(colander.String())
        with pytest.raises(Invalid):
            validator(node, u"")
        with pytest.raises(Invalid):
            validator(node, u"d?")


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




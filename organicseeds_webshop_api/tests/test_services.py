import unittest
import yaml
import yaml2json
from webtest import TestApp
from pyramid import testing

from organicseeds_webshop_api import main
from organicseeds_webshop_api import schemata


def yaml_to_json(yamlstring):
    yamldata = yaml.load(yamlstring)
    jsondata = yaml2json.convertArrays(yamldata)
    return jsondata


class TestServicesFunctional(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(main({"zodbconn.uri": "memory://"}))

    def test_categories_put(self):
        jsondata = yaml_to_json(schemata.CATEGORIES_EXAMPLE_YAML)
        self.app.post_json('/categories', jsondata)

    def test_items_put(self):
        jsondata = yaml_to_json(schemata.ITEMS_POST_EXAMPLE_YAML)
        self.app.post_json('/items', jsondata)


class TestServicesIntegration(unittest.TestCase):

    def setUp(self):
        import organicseeds_webshop_api
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request, settings = {"zodbconn.uri": "memory://"})
        self.config.include("pyramid_zodbconn")
        self.config.include(organicseeds_webshop_api.utilities)
        self.config.include(organicseeds_webshop_api.models)
        self.request.root = organicseeds_webshop_api.root_factory(self.request)

    def tearDown(self):
        testing.tearDown()

    def test_items_post(self):
        from organicseeds_webshop_api.services import items_post
        import json
        request = self.request
        request.context = testing.DummyResource()
        jsondata = yaml_to_json(schemata.ITEMS_POST_EXAMPLE_YAML)
        jsonstr = json.dumps(jsondata)
        request.body = jsonstr
        response =  items_post(request)
        assert(response == {'test': 'succeeded'})

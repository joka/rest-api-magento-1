import unittest
import json
import yaml
import yaml2json
import pytest
from webtest import TestApp
from webtest.app import AppError
from pyramid import testing

from organicseeds_webshop_api import main
from organicseeds_webshop_api import schemata


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

    def tearDown(self):
        testing.tearDown()

    def test_items_post(self):
        from organicseeds_webshop_api.services import items_post
        jsondata = yaml_to_json(schemata.ITEMS_POST_EXAMPLE_YAML)
        jsonstr = json.dumps(jsondata)
        self.request.body = jsonstr
        response =  items_post(self.request)
        assert(response == {'test': 'succeeded'})


class TestServicesFunctional(unittest.TestCase):

    def setUp(self):
        self.app = TestApp(main({"zodbconn.uri": "memory://"}))

    def test_categories_put(self):
        jsondata = yaml_to_json(schemata.CATEGORIES_EXAMPLE_YAML)
        self.app.post_json('/categories', jsondata)

    def test_items_put(self):
        jsondata = yaml_to_json(schemata.ITEMS_POST_EXAMPLE_YAML)
        resp = self.app.post_json('/items', jsondata)
        assert resp.status_int == 200

    def test_items_post_validate_vpe_type_id(self):
        jsondata = yaml_to_json(schemata.ITEMS_POST_EXAMPLE_YAML)
        jsondata["vpe_types"][0]["id"] = "wrongid"
        with  pytest.raises(AppError):
            self.app.post_json('/items', jsondata)

    def test_items_post_validate_unit_of_measure_id(self):
        jsondata = yaml_to_json(schemata.ITEMS_POST_EXAMPLE_YAML)
        jsondata["unit_of_measures"][0]["id"] = "wrongid"
        with  pytest.raises(AppError):
            self.app.post_json('/items', jsondata)

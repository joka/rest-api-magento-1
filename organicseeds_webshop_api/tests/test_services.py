import unittest
import json
import yaml
import yaml2json
import pytest
import os.path
from webtest import TestApp
from webtest.app import AppError
from pyramid import testing


def yaml_to_json(yamlstring):
    yamldata = yaml.load(yamlstring)
    jsondata = yaml2json.convertArrays(yamldata)
    return jsondata


def setup_integration():
    import organicseeds_webshop_api
    request = testing.DummyRequest()
    request.context = testing.DummyResource()
    config = testing.setUp(request=request, settings = {"zodbconn.uri": "memory://"})
    config.include("pyramid_zodbconn")
    config.include(organicseeds_webshop_api.utilities)
    config.include(organicseeds_webshop_api.models)
    request.root = organicseeds_webshop_api.root_factory(request)
    return dict(request=request,
                config=config)


def set_testfile(testfile):
    import organicseeds_webshop_api
    testfilepath = os.path.join(organicseeds_webshop_api.tests.__path__[0] + testfile)
    testfile = open(testfilepath, "r")
    testdata = yaml.load(testfile)
    return dict(testdata=testdata,
                testfile=testfile)


class TestServicesItemsIntegration(unittest.TestCase):

    def setUp(self):
        self.__dict__.update(setup_integration())
        self.__dict__.update(set_testfile("/testdata/items_post.yaml"))

    def tearDown(self):
        testing.tearDown()
        self.testfile.close()

    def test_post(self):
        from organicseeds_webshop_api.services import items_post
        jsonstr = json.dumps(self.testdata)
        self.request.body = jsonstr
        response =  items_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesCategoriesIntegration(unittest.TestCase):

    def setUp(self):
        self.__dict__.update(setup_integration())
        self.__dict__.update(set_testfile("/testdata/categories_post.yaml"))

    def tearDown(self):
        testing.tearDown()
        self.testfile.close()

    def test_post(self):
        from organicseeds_webshop_api.services import categories_post
        jsonstr = json.dumps(self.testdata)
        self.request.body = jsonstr
        response = categories_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemGroupsIntegration(unittest.TestCase):

    def setUp(self):
        self.__dict__.update(setup_integration())
        self.__dict__.update(set_testfile("/testdata/item_groups_post.yaml"))

    def tearDown(self):
        testing.tearDown()
        self.testfile.close()

    def test_post(self):
        from organicseeds_webshop_api.services import item_groups_post
        jsonstr = json.dumps(self.testdata)
        self.request.body = jsonstr
        response = item_groups_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemsFunctional(unittest.TestCase):

    def setUp(self):
        from organicseeds_webshop_api import main
        self.app = TestApp(main({"zodbconn.uri": "memory://"}))
        self.__dict__.update(set_testfile("/testdata/items_post.yaml"))

    def tearDown(self):
        self.testfile.close()

    def test_post(self):
        jsondata = self.testdata
        resp = self.app.post_json('/items', jsondata)
        assert resp.status_int == 200

    def test_post_error(self):
        jsondata = self.testdata
        jsondata["vpe_types"][0]["id"] = "wrongid"
        with pytest.raises(AppError):
            self.app.post_json('/items', jsondata)


class TestServicesItemGroupsFunctional(unittest.TestCase):

    def setUp(self):
        from organicseeds_webshop_api import main
        self.app = TestApp(main({"zodbconn.uri": "memory://"}))
        self.__dict__.update(set_testfile("/testdata/item_groups_post.yaml"))

    def tearDown(self):
        self.testfile.close()

    def test_post(self):
        jsondata = self.testdata
        resp = self.app.post_json('/item_groups', jsondata)
        assert resp.status_int == 200


class TestServicesCategoriesFunctional(unittest.TestCase):

    def setUp(self):
        from organicseeds_webshop_api import main
        self.app = TestApp(main({"zodbconn.uri": "memory://"}))
        self.__dict__.update(set_testfile("/testdata/categories_post.yaml"))

    def tearDown(self):
        self.testfile.close()

    def test_post(self):
        jsondata = self.testdata
        resp = self.app.post_json('/categories', jsondata)
        assert resp.status_int == 200

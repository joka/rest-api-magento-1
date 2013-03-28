import unittest
import yaml
import yaml2json
import os.path
from webtest import TestApp
from pyramid import testing
from cornice.errors import Errors


def yaml_to_json(yamlstring):
    yamldata = yaml.load(yamlstring)
    jsondata = yaml2json.convertArrays(yamldata)
    return jsondata


def setup_integration():
    import organicseeds_webshop_api
    request = testing.DummyRequest()
    request.context = testing.DummyResource()
    request.errors = Errors(request)
    config = testing.setUp(request=request, settings = {"zodbconn.uri": "memory://"})
    config.include("pyramid_zodbconn")
    config.include(organicseeds_webshop_api.utilities)
    config.include(organicseeds_webshop_api.models)
    request.root = organicseeds_webshop_api.root_factory(request)
    return dict(request=request,
                config=config)


def setup_functional():
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


class IntegrationTestCase(unittest.TestCase):

    testdatafilepath =  "/testdata/.empty"

    def setUp(self):
        self.__dict__.update(setup_integration())
        self.__dict__.update(set_testfile(self.testdatafilepath))

    def tearDown(self):
        testing.tearDown()
        self.testfile.close()
        self.request = None


class FunctionalTestCase(unittest.TestCase):

    testdatafilepath =  "/testdata/.empty"

    def setUp(self):
        from organicseeds_webshop_api import main
        self.app = TestApp(main({"zodbconn.uri": "memory://"}))
        self.__dict__.update(set_testfile(self.testdatafilepath))

    def tearDown(self):
        self.testfile.close()

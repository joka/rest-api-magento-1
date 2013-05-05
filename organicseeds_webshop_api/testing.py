import unittest
import yaml
import yaml2json
from webtest import TestApp
from pyramid import testing
from cornice.errors import Errors


def testconfig():
    import organicseeds_webshop_api
    module = organicseeds_webshop_api.__path__[0]
    whiz = module + "/../../../bin/whiz"
    config = {"zodbconn.uri": "memory://",
              "magento_whiz_script": whiz,
              "magento_rpc_user": u"webshop_api",
              "magento_rpc_secret":  u"oxXCcvIAhdXcw",
              "magento_apiurl": "http://hobby.developlocal.sativa.jokasis.de/"
              }
    return config


def yaml_to_json(yamlstring):
    yamldata = yaml.load(yamlstring)
    jsondata = yaml2json.convertArrays(yamldata)
    return jsondata


def setup_integration():
    import organicseeds_webshop_api
    request = testing.DummyRequest()
    request.context = testing.DummyResource()
    request.errors = Errors(request)
    config = testing.setUp(request=request,
                           settings=testconfig())
    config.include("pyramid_zodbconn")
    request.root = organicseeds_webshop_api.root_factory(request)
    app_root = request.root.app_root
    return dict(request=request,
                config=config,
                app_root=app_root)


def get_file(path):
    import organicseeds_webshop_api
    import os
    full_path = os.path.join(organicseeds_webshop_api.tests.__path__[0] + path)
    return open(full_path, "r")


def set_testfile(testfilepath):
    testfile = get_file(testfilepath)
    testdata = yaml.load(testfile)
    return dict(testdata=testdata,
                testfile=testfile)


class IntegrationTestCase(unittest.TestCase):

    testdatafilepath = "/testdata/.empty"

    def setUp(self):
        self.__dict__.update(setup_integration())
        self.__dict__.update(set_testfile(self.testdatafilepath))

    def tearDown(self):
        testing.tearDown()
        self.testfile.close()
        self.request.root.app_root["categories"].clear()
        self.request.root.app_root["items"].clear()
        self.request.root.app_root["item_groups"].clear()
        self.request.root.app_root["vpe_types"].clear()
        self.request.root.app_root["unit_of_measures"].clear()
        self.request = None


class MagentoIntegrationTestCase(IntegrationTestCase):

    def setUp(self):
        super(MagentoIntegrationTestCase, self).setUp()
        from organicseeds_webshop_api import magentoapi
        items_proxy = magentoapi.Items(self.request)
        items_proxy.__enter__()
        item_groups_proxy = magentoapi.ItemGroups(self.request)
        categories_proxy = magentoapi.Categories(self.request)
        item_groups_proxy.client = items_proxy.client
        item_groups_proxy.session = items_proxy.session
        categories_proxy.client = items_proxy.client
        categories_proxy.session = items_proxy.session
        self.items_proxy = items_proxy
        self.item_groups_proxy = item_groups_proxy
        self.categories_proxy = categories_proxy

    def tearDown(self):
        from xmlrpclib import Fault
        try:
            self.items_proxy.delete_all()
            self.item_groups_proxy.delete_all()
            self.categories_proxy.delete_all()
        except Fault:
            pass
        self.items_proxy.__exit__(None, None, None)
        super(MagentoIntegrationTestCase, self).tearDown()


class FunctionalTestCase(unittest.TestCase):

    testdatafilepath = "/testdata/.empty"

    def setUp(self):
        from organicseeds_webshop_api import main
        self.app = TestApp(main(testconfig()))
        self.__dict__.update(set_testfile(self.testdatafilepath))

    def tearDown(self):
        self.testfile.close()

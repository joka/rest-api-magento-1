import unittest
import yaml
import yaml2json
from webtest import TestApp
from pyramid import testing
from cornice.errors import Errors


def create_category(appstruct, request, categoriesproxy=None):
    from organicseeds_webshop_api.models import Category
    cat = Category()
    cat.from_appstruct(appstruct)
    request.root.app_root["categories"][appstruct["id"]] = cat
    if categoriesproxy:
        cat.webshop_id = categoriesproxy.create([appstruct])[0]
    return cat


def create_item(appstruct, request, itemsproxy=None):
    from organicseeds_webshop_api.models import Item
    item = Item()
    item.from_appstruct(appstruct)
    request.root.app_root["items"][appstruct["id"]] = item
    if itemsproxy:
        item.webshop_id = itemsproxy.create([appstruct])[0]
    return item


def create_item_group(appstruct, request, itemgroupsproxy=None):
    from organicseeds_webshop_api.models import ItemGroup
    item_group = ItemGroup()
    item_group.from_appstruct(appstruct)
    request.root.app_root["item_groups"][appstruct["id"]] = item_group
    if itemgroupsproxy:
        item_group.webshop_id = itemgroupsproxy.create([appstruct])[0]
    return item_group


def create_vpe_type(appstruct, request):
    from organicseeds_webshop_api.models import EntityData
    vpe_type = EntityData()
    vpe_type.from_appstruct(appstruct)
    request.root.app_root["vpe_types"][appstruct["id"]] = vpe_type
    return vpe_type


def create_unit_of_measure(appstruct, request):
    from organicseeds_webshop_api.models import EntityData
    unit_of_measure = EntityData()
    unit_of_measure.from_appstruct(appstruct)
    request.root.app_root["unit_of_measures"][appstruct["id"]] =\
        unit_of_measure
    return unit_of_measure


def create_all_testdata_items(request):
    from organicseeds_webshop_api.testing import set_testfile
    vpes_ = set_testfile("/testdata/vpe_types_post.yaml")["testdata"]
    units_ = set_testfile("/testdata/unit_of_measures_post.yaml")["testdata"]
    groups_ = set_testfile("/testdata/item_groups_post.yaml")["testdata"]
    items_ = set_testfile("/testdata/items_post.yaml")["testdata"]
    vpe = create_vpe_type(vpes_["vpe_types"][0], request)
    unit = create_unit_of_measure(units_["unit_of_measures"][0], request)
    item = create_item(items_["items"][0], request)
    group = create_item_group(groups_["item_groups"][0], request)
    item.__parent__ = group
    group.__children__.append(item)
    item.vpe_type = vpe
    item.unit_of_measure = unit
    item.quality = group["qualities"][0]
    return vpe, unit, item, group


def testconfig():
    import organicseeds_webshop_api
    module = organicseeds_webshop_api.__path__[0]
    whiz = module + "/../../../bin/whiz"
    config = {"zodbconn.uri": "memory://",
              "magento_whiz_script": whiz,
              "magento_rpc_user": u"webshop_api",
              "magento_rpc_secret": u"oxXCcvIAhdXcw",
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

        def clear_entities(key, request):
            for x in self.request.root.app_root[key].values():
                if hasattr(x, "__parent__"):
                    x.__parent__ is None
                if hasattr(x, "__children__"):
                    x.__children__ == []
            request.root.app_root[key].clear()

        clear_entities("categories", self.request)
        clear_entities("items", self.request)
        clear_entities("item_groups", self.request)
        clear_entities("vpe_types", self.request)
        clear_entities("unit_of_measures", self.request)
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

import copy
import pytest
from organicseeds_webshop_api.testing import (
    MagentoIntegrationTestCase,
)


def create_item(appstruct, request):
    from organicseeds_webshop_api.models import Item
    item = Item()
    item.from_appstruct(appstruct)
    request.root.app_root["items"][appstruct["id"]] = item
    return item


class TestMagentoProxyIntegrationServerload(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    @pytest.mark.loadtest
    def test_load_create_items_time_10(self):
        proxy = self.items_proxy
        import time
        start = time.time()
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 10):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstruct_["title"]["fr"] = u"titlefr" + str(x)
            appstruct_["title"]["de"] = u"titlede" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        print("\ncreating items")
        webshop_ids = proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id
        print("\nupdateing items")
        proxy.update_shops(webshop_ids, appstructs)
        print("\nlinking item parents")
        proxy.link_item_parents(webshop_ids, appstructs)
        end = time.time()
        print("\n\nTime to create 10 items:")
        print(end - start)
        print("\n")

    @pytest.mark.loadtest
    def test_load_create_items_99(self):
        proxy = self.items_proxy
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 99):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstruct_["title"]["fr"] = u"titlefr" + str(x)
            appstruct_["title"]["de"] = u"titlede" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id
        proxy.update_shops(webshop_ids, appstructs)

    @pytest.mark.loadtest
    def test_load_create_items_100(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 100):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstruct_["title"]["fr"] = u"titlefr" + str(x)
            appstruct_["title"]["de"] = u"titlede" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.items_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

    @pytest.mark.loadtest
    def test_load_create_items_101(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 101):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstruct_["title"]["fr"] = u"titlefr" + str(x)
            appstruct_["title"]["de"] = u"titlede" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.items_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

    #@pytest.mark.loadtest
    #def test_load_create_items_9(self):
        #appstruct = self.testdata["items"][0]
        #appstructs = []
        #items = []
        #for x in range(0, 9):
            #appstruct_ = copy.deepcopy(appstruct)
            #appstruct_["id"] = u"id" + str(x)
            #appstruct_["sku"] = u"sku" + str(x)
            #appstruct_["title"]["default"] = u"title" + str(x)
            #appstruct_["title"]["fr"] = u"titlefr" + str(x)
            #appstruct_["title"]["de"] = u"titlede" + str(x)
            #appstructs.append(appstruct_)
            #items.append(create_item(appstruct_, self.request))
        #webshop_ids = self.items_proxy.create(appstructs)
        #for i, webshop_id in enumerate(webshop_ids):
            #items[i].webshop_id = webshop_id

    #@pytest.mark.loadtest
    #def test_load_create_items_10(self):
        #appstruct = self.testdata["items"][0]
        #appstructs = []
        #items = []
        #for x in range(0, 10):
            #appstruct_ = copy.deepcopy(appstruct)
            #appstruct_["id"] = u"id" + str(x)
            #appstruct_["sku"] = u"sku" + str(x)
            #appstruct_["title"]["default"] = u"title" + str(x)
            #appstruct_["title"]["fr"] = u"titlefr" + str(x)
            #appstruct_["title"]["de"] = u"titlede" + str(x)
            #appstructs.append(appstruct_)
            #items.append(create_item(appstruct_, self.request))
        #webshop_ids = self.items_proxy.create(appstructs)
        #for i, webshop_id in enumerate(webshop_ids):
            #items[i].webshop_id = webshop_id

    #@pytest.mark.loadtest
    #def test_load_create_items_11(self):
        #appstruct = self.testdata["items"][0]
        #appstructs = []
        #items = []
        #for x in range(0, 11):
            #appstruct_ = copy.deepcopy(appstruct)
            #appstruct_["id"] = u"id" + str(x)
            #appstruct_["sku"] = u"sku" + str(x)
            #appstruct_["title"]["default"] = u"title" + str(x)
            #appstruct_["title"]["fr"] = u"titlefr" + str(x)
            #appstruct_["title"]["de"] = u"titlede" + str(x)
            #appstructs.append(appstruct_)
            #items.append(create_item(appstruct_, self.request))
        #webshop_ids = self.items_proxy.create(appstructs)
        #for i, webshop_id in enumerate(webshop_ids):
            #items[i].webshop_id = webshop_id

    #@pytest.mark.loadtest
    #def test_load_create_items_20(self):
        #appstruct = self.testdata["items"][0]
        #appstructs = []
        #items = []
        #for x in range(0, 20):
            #appstruct_ = copy.deepcopy(appstruct)
            #appstruct_["id"] = u"id" + str(x)
            #appstruct_["sku"] = u"sku" + str(x)
            #appstruct_["title"]["default"] = u"title" + str(x)
            #appstruct_["title"]["fr"] = u"titlefr" + str(x)
            #appstruct_["title"]["de"] = u"titlede" + str(x)
            #appstructs.append(appstruct_)
            #items.append(create_item(appstruct_, self.request))
        #webshop_ids = self.items_proxy.create(appstructs)
        #for i, webshop_id in enumerate(webshop_ids):
            #items[i].webshop_id = webshop_id

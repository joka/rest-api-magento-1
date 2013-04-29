import copy
import pytest
from organicseeds_webshop_api import magentoapi
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
    magento_proxy_class = magentoapi.Items

    @pytest.mark.loadtest
    def test_load_create_items_100(self):
        proxy = self.magento_proxy
        import time
        start = time.time()
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 100):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id
        proxy.delete(appstructs)
        end = time.time()
        print("\n\nTime to create and delete 100 items:")
        print(end - start)
        print("\n")

    @pytest.mark.loadtest
    def test_load_create_items_6(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 6):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.magento_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

    @pytest.mark.loadtest
    def test_load_create_items_7(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 7):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.magento_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

    @pytest.mark.loadtest
    def test_load_create_items_8(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 8):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.magento_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

    @pytest.mark.loadtest
    def test_load_create_items_9(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 9):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.magento_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

    @pytest.mark.loadtest
    def test_load_create_items_10(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 10):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.magento_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

    @pytest.mark.loadtest
    def test_load_create_items_11(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 11):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.magento_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

    @pytest.mark.loadtest
    def test_load_create_items_20(self):
        appstruct = self.testdata["items"][0]
        appstructs = []
        items = []
        for x in range(0, 20):
            appstruct_ = copy.deepcopy(appstruct)
            appstruct_["id"] = u"id" + str(x)
            appstruct_["sku"] = u"sku" + str(x)
            appstruct_["title"]["default"] = u"title" + str(x)
            appstructs.append(appstruct_)
            items.append(create_item(appstruct_, self.request))
        webshop_ids = self.magento_proxy.create(appstructs)
        for i, webshop_id in enumerate(webshop_ids):
            items[i].webshop_id = webshop_id

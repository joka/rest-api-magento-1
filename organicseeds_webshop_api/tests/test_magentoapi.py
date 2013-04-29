# -*- coding: utf-8 -*-
import copy
import pytest
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    MagentoIntegrationTestCase,
)
from organicseeds_webshop_api import magentoapi


def create_item(appstruct, request):
    from organicseeds_webshop_api.models import Item
    item = Item()
    item.from_appstruct(appstruct)
    request.root.app_root["items"][appstruct["id"]] = item
    return item


def create_item_group(appstruct, request):
    from organicseeds_webshop_api.models import ItemGroup
    item_group = ItemGroup()
    item_group.from_appstruct(appstruct)
    request.root.app_root["item_groups"][appstruct["id"]] = item_group
    return item_group


def create_category(appstruct, request):
    from organicseeds_webshop_api.models import Category
    cat = Category()
    cat.from_appstruct(appstruct)
    request.root.app_root["categories"][appstruct["id"]] = cat
    return cat


class TestMagentoAPIHelpersIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_magentoapi_get_websites_ids_multiple(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"id": "testitem",
                     "shops": [("ch_hobby", True), ("ch_profi", True),
                               ("fr_hobby", True),
                               ("fr_profi", False),
                               ("de_hobby", False)
                               ]}
        assert magentoapi.get_website_ids(appstruct) == \
            [u"ch_website", u"fr_website"]

    def test_magentoapi_get_websites_ids_none(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"id": "testitem",
                     "shops": []}
        assert magentoapi.get_website_ids(appstruct) == []

    def test_magentoapi_get_category_ids_multiple(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"id": "testitem",
                     "category_ids": [u"cat1", u"cat2"]}
        item = create_item(appstruct, self.request)
        category = create_category({"id": "cat1"}, self.request)
        category.webshop_id = 2
        assert magentoapi.get_category_ids(item, self.request) == [2]

    def test_magentoapi_get_category_ids_none(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"id": "testitem"}
        item = create_item(appstruct, self.request)
        assert magentoapi.get_category_ids(item, self.request) == []

    def test_magentoapi_get_all_website_ids(self):
        from organicseeds_webshop_api import magentoapi
        websites = magentoapi.get_all_website_ids()
        assert websites == ["ch_website", "de_website", "fr_website"]


class TestMagentoAPIMagentoAPIIntegration(MagentoIntegrationTestCase):

    magento_proxy_class = magentoapi.MagentoAPI

    def test_magentoapi_magentoapi_multi_call(self):
        proxy = self.magento_proxy
        calls = []
        response = proxy.multi_call(calls)
        assert response == []
        for x in range(0, 2):
            calls.append(["store.list"])
        response = proxy.multi_call(calls)
        assert 'website_id' in response[0][0]
        response = proxy.multi_call(calls)
        calls = []
        for x in range(0, 11):
            calls.append(['store.list'])
        response = proxy.multi_call(calls)
        assert 'website_id' in response[0][0]
        calls = []
        for x in range(0, 20):
            calls.append(["store.list"])
        response = proxy.multi_call(calls)
        assert 'website_id' in response[0][0]

    def test_magentoapi_magentoapi_multi_call_error(self):
        calls = [["wrong_metho"]]
        with pytest.raises(Exception):
            self.magento_proxy.multi_call(calls)


class TestMagentoAPIItemsIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")
    magento_proxy_class = magentoapi.Items

    def test_magentoapi_create_items(self):
        appstruct = self.testdata["items"][0]
        webshop_id = self.magento_proxy.create([appstruct])[0]
        assert webshop_id > 0

    def test_magentoapi_to_update_data(self):
        appstruct = self.testdata["items"][0]
        data = self.magento_proxy._to_update_data(appstruct)
        assert set(data.keys()) == set(['name', 'weight', 'price',
                                        'tax_class_id', 'short_description',
                                        'url_key', 'description'])
        assert set(data.values()) == set(['title', 0.25, 4.3, 2,
                                          'kurzbeschreibung', u'title',
                                          u'Ausfuehrliche Beschreibung'])

        appstruct = {}
        data = self.magento_proxy._to_update_data(appstruct)
        assert data == {}

    def test_magentoapi_to_update_translation_data(self):
        appstruct = self.testdata["items"][0]
        data = self.magento_proxy._to_update_translation_data(appstruct, "fr")
        assert data == {'name': 'titlefr', 'short_description': 'dscription',
                        'url_key': u'titlefr'}

    def test_magentoapi_to_create_data(self):
        appstruct = {}
        data = self.magento_proxy._to_create_data(appstruct)
        default_data = {'status': 0,
                        'websites': ['ch_website', 'de_website', 'fr_website'],
                        'visibility': 4}
        assert data == default_data

    def test_magentoapi_update_items(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["items"][0]
        item = create_item(appstruct, self.request)
        item.webshop_id = proxy.create([appstruct])[0]

        updates = [{"id": appstruct["id"],
                    "title": {"default": u"New unique_name"}}]
        proxy.update(updates)
        results = proxy.single_call('catalog_product.list')
        assert results[0]["name"] == u"New unique_name"

    def test_magentoapi_delete_items(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["items"][0]
        item = create_item(appstruct, self.request)
        item.webshop_id = proxy.create([appstruct])[0]

        proxy.delete([{"id": appstruct["id"]}])
        results = proxy.single_call('catalog_product.list')
        assert results == []


class TestMagentoAPIItemGroupsIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")
    magento_proxy_class = magentoapi.ItemGroups

    def test_magentoapi_create_item_groups(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["item_groups"][0]
        appstruct["title"]["default"] = u"unique_name"
        webshop_id = proxy.create([appstruct])[0]
        assert webshop_id > 0

    def test_magentoapi_update_item_groups(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["item_groups"][0]
        appstruct = self.testdata["item_groups"][0]
        appstruct["title"]["default"] = u"unique_name"
        item_group = create_item_group(appstruct, self.request)
        item_group.webshop_id = proxy.create([appstruct])[0]

        update = {"id": appstruct["id"],
                  "title": {"default": u"New unique_name"}}
        proxy.update([update])
        results = proxy.single_call('catalog_product.list')
        assert results[0]["name"] == u"New unique_name"

    def test_magentoapi_delete_item_groups(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["item_groups"][0]
        item_group = create_item_group(appstruct, self.request)
        item_group.webshop_id = proxy.create([appstruct])[0]

        proxy.delete([{"id": appstruct["id"]}])
        item_groups = proxy.single_call('catalog_product.list')
        assert item_groups == []


class TestMagentoAPICategoriesIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")
    magento_proxy_class = magentoapi.Categories

    def test_magentoapi_to_create_data(self):
        appstruct = {}
        data = self.magento_proxy._to_create_data(appstruct)
        default_data = {"available_sort_by": ["position", "name", "price"],
                        "default_sort_by": "position",
                        "include_in_menu": 1,
                        "is_active": 0}
        assert data == default_data

    def test_magentoapi_create_categories(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["categories"][0]
        appstruct["parent_id"] = None
        appstruct["title"]["default"] = u"unique_name"
        webshop_id = proxy.create([appstruct])[0]
        assert webshop_id > 0

    def test_magentoapi_update_categories(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["categories"][0]
        appstruct["title"]["default"] = u"unique_name"
        category = create_category(appstruct, self.request)
        category.webshop_id = proxy.create([appstruct])[0]

        update = {"id": appstruct["id"],
                  "title": {"default": u"New unique_name"}}
        results = proxy.update([update])
        assert results[0] is True

    def test_magentoapi_delete_categories(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["categories"][0]
        category = create_category(appstruct, self.request)
        category.webshop_id = proxy.create([appstruct])[0]

        proxy.delete([{"id": appstruct["id"]}])
        result = proxy.single_call('catalog_category.level')
        assert category.webshop_id not in [x["category_id"] for x in result]

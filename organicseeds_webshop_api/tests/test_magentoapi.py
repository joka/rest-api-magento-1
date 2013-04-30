# -*- coding: utf-8 -*-
import pytest
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    MagentoIntegrationTestCase,
)
from organicseeds_webshop_api import magentoapi


def create_item(appstruct, request, proxy=None):
    from organicseeds_webshop_api.models import Item
    item = Item()
    item.from_appstruct(appstruct)
    request.root.app_root["items"][appstruct["id"]] = item
    if proxy:
        item.webshop_id = int(proxy.single_call("catalog_product.create",
                              ["simple", 4, appstruct["sku"], []]))
    return item


def create_item_group(appstruct, request, proxy=None):
    from organicseeds_webshop_api.models import ItemGroup
    item_group = ItemGroup()
    item_group.from_appstruct(appstruct)
    request.root.app_root["item_groups"][appstruct["id"]] = item_group
    if proxy:
        item_group.webshop_id = int(
            proxy.single_call("catalog_product.create",
                              ["grouped", 4, appstruct["id"], []]))
    return item_group


def create_category(appstruct, request, proxy=None):
    from organicseeds_webshop_api.models import Category
    cat = Category()
    cat.from_appstruct(appstruct)
    request.root.app_root["categories"][appstruct["id"]] = cat
    if proxy:
        cat.webshop_id = int(
            proxy.single_call("catalog_category.create",
                              [2, {"name": appstruct["id"],
                                   "available_sort_by": ["position"],
                                   "include_in_menu": 1,
                                   "default_sort_by": "position",
                                   "is_active": 0},
                               None]))
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

    def test_magentoapi_create_items(self):
        appstruct = self.testdata["items"][0]
        webshop_id = self.magento_proxy.create([appstruct])[0]
        assert webshop_id > 0

    def test_magentoapi_link_item_with_item_group_parents(self):
        proxy = self.magento_proxy
        appstruct = {"id": u"item", "sku": u"itemsku", "parent_id": "parent"}
        item = create_item(appstruct, self.request, proxy)
        parent = create_item_group({"id": "parent"}, self.request, proxy)
        try:
            proxy.link_item_parents([item.webshop_id], [appstruct])
            children = proxy.single_call("catalog_product_link.list",
                                         ["grouped", parent.webshop_id])
            assert item.webshop_id in [int(x["product_id"]) for x in children]
        finally:
            proxy.single_call("catalog_product.delete", ["parent"])  # cleanup

    def test_magentoapi_link_items_with_category_parents(self):
        proxy = self.magento_proxy
        appstruct = {"id": u"item", "sku": u"itemsku", "parent_id": "parent"}
        item = create_item(appstruct, self.request, proxy)
        parent = create_category({"id": "parent"}, self.request, proxy)
        try:
            proxy.link_item_parents([item.webshop_id], [appstruct])
            children = proxy.single_call("category.assignedProducts",
                                         [parent.webshop_id])
            assert item.webshop_id in [int(x["product_id"]) for x in children]
        finally:
            proxy.single_call("catalog_category.delete", [parent.webshop_id])

    def test_magentoapi_update_items(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["items"][0]
        create_item(appstruct, self.request, proxy)

        updates = [{"id": appstruct["id"],
                    "title": {"default": u"New unique_name"}}]
        proxy.update(updates)
        results = proxy.single_call('catalog_product.list')
        assert results[0]["name"] == u"New unique_name"

    def test_magentoapi_delete_items(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["items"][0]
        create_item(appstruct, self.request, proxy)

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
        create_item_group(appstruct, self.request, proxy)

        update = {"id": appstruct["id"],
                  "title": {"default": u"New unique_name"}}
        proxy.update([update])
        results = proxy.single_call('catalog_product.list')
        assert results[0]["name"] == u"New unique_name"

    def test_magentoapi_delete_item_groups(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["item_groups"][0]
        create_item_group(appstruct, self.request, proxy)

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
        webshop_id = proxy.create([appstruct])[0]
        default_children = proxy.single_call("catalog_category.level",[None, None, 2])
        assert webshop_id == int(default_children[0]["category_id"])

    def test_magentoapi_link_category_parents(self):
        proxy = self.magento_proxy
        appstruct_p = {"id": u"parent", "parent_id": None}
        appstruct_c = {"id": u"child", "parent_id": u"parent"}
        category_p = create_category(appstruct_p, self.request, proxy)
        category_c = create_category(appstruct_c, self.request, proxy)

        proxy.link_category_parents([category_c.webshop_id,
                                     category_p.webshop_id],
                                    [appstruct_c, appstruct_p])
        level1 = proxy.single_call("catalog_category.level", [None, None, 2])
        assert category_p.webshop_id == int(level1[0]["category_id"])
        level2 = proxy.single_call("catalog_category.level",
                                   [None, None, category_p.webshop_id])
        assert category_c.webshop_id == int(level2[0]["category_id"])

    def test_magentoapi_update_categories(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["categories"][0]
        appstruct["title"]["default"] = u"unique_name"
        create_category(appstruct, self.request, proxy)

        update = {"id": appstruct["id"],
                  "title": {"default": u"New unique_name"}}
        results = proxy.update([update])
        assert results[0] is True

    def test_magentoapi_delete_categories(self):
        proxy = self.magento_proxy
        appstruct = self.testdata["categories"][0]
        category = create_category(appstruct, self.request, proxy)

        proxy.delete([{"id": appstruct["id"]}])
        result = proxy.single_call('catalog_category.level')
        assert category.webshop_id not in [x["category_id"] for x in result]

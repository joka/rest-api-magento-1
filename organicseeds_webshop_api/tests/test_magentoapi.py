# -*- coding: utf-8 -*-
import pytest
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    MagentoIntegrationTestCase,
)
from organicseeds_webshop_api import magentoapi


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


def create_category(appstruct, request, categoriesproxy=None):
    from organicseeds_webshop_api.models import Category
    cat = Category()
    cat.from_appstruct(appstruct)
    request.root.app_root["categories"][appstruct["id"]] = cat
    if categoriesproxy:
        cat.webshop_id = categoriesproxy.create([appstruct])[0]
    return cat


class TestMagentoAPIHelpersIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_magentoapi_get_storeviews(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"shops": [("ch_hobby", True),
                               ("ch_profi", False),
                               ("fr_hobby", True)]}
        wanted = set([("de_ch_hobby", True, "de", "ch"),
                      ("fr_ch_hobby", True, "fr", "ch"),
                      ("it_ch_hobby", True, "it", "ch"),
                      ("de_ch_profi", False, "de", "ch"),
                      ("fr_ch_profi", False, "fr", "ch"),
                      ("it_ch_profi", False, "it", "ch"),
                      ("fr_fr_hobby", True, "fr", "fr")])
        assert set(magentoapi.get_storeviews(appstruct)) == wanted

    def test_magentoapi_get_storeviews_none(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {}
        assert magentoapi.get_storeviews(appstruct) == []

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

    def test_magentoapi_magentoapi_multi_call(self):
        proxy = self.items_proxy
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
            self.items_proxy.multi_call(calls)


class TestMagentoAPIItemsIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_magentoapi_items_to_update_shops_data(self):
        proxy = self.items_proxy
        appstruct = self.testdata["items"][0]
        data = proxy._to_update_shops_data(appstruct, "fr", "ch")
        assert data == {'name': 'titlefr',
                        'short_description': 'dscription',
                        'url_key': u'titlefr',
                        'price': 2.0}
        data = proxy._to_update_shops_data(appstruct, "default", "default")
        assert data == {'name': 'title',
                        'short_description': 'kurzbeschreibung',
                        'url_key': u'title',
                        'description': 'Ausfuehrliche Beschreibung'
                        }

    def test_magentoapi_items_to_update_data(self):
        appstruct = self.testdata["items"][0]
        data = self.items_proxy._to_update_data(appstruct)
        assert ('weight', 0.25) in data.items()
        assert ('url_key', u'title') in data.items()
        appstruct = {}
        data = self.items_proxy._to_update_data(appstruct)
        assert data == {}

    def test_magentoapi_items_to_create_data(self):
        appstruct = {}
        data = self.items_proxy._to_create_data(appstruct)
        assert ('status', 1) in data.items()
        assert ('websites', ['ch_website', 'de_website', 'fr_website'])\
            in data.items()
        assert ('visibility', 1) in data.items()

    def test_magentoapi_create_items(self):
        proxy = self.items_proxy
        appstruct = self.testdata["items"][0]
        webshop_id = proxy.create([appstruct])[0]
        result = proxy.single_call('catalog_product.info', [webshop_id])
        assert result["websites"] == ['2', '3', '5']
        assert result["price"] is None
        assert result["status"] == '1'

    def test_magentoapi_link_item_with_item_group_parents(self):
        proxy = self.items_proxy
        appstruct = {"id": u"item", "sku": u"itemsku", "parent_id": "parent"}
        item = create_item(appstruct, self.request, proxy)
        parent = create_item_group({"id": "parent"}, self.request,
                                   self.item_groups_proxy)
        try:
            proxy.link_item_parents([item.webshop_id], [appstruct])
            children = proxy.single_call("catalog_product_link.list",
                                         ["grouped", parent.webshop_id])
            assert item.webshop_id in [int(x["product_id"]) for x in children]
        finally:
            proxy.single_call("catalog_product.delete", ["parent"])  # cleanup

    def test_magentoapi_link_items_with_category_parents(self):
        proxy = self.items_proxy
        appstruct = {"id": u"item", "sku": u"itemsku", "parent_id": "parent"}
        item = create_item(appstruct, self.request, proxy)
        parent = create_category(
            {"id": "parent", "title": {"default": "parent"}}, self.request,
            self.categories_proxy)
        try:
            proxy.link_item_parents([item.webshop_id], [appstruct])
            children = proxy.single_call("category.assignedProducts",
                                         [parent.webshop_id])
            assert item.webshop_id in [int(x["product_id"]) for x in children]
        finally:
            proxy.single_call("catalog_category.delete", [parent.webshop_id])

    def test_magentoapi_items_update(self):
        proxy = self.items_proxy
        appstruct = self.testdata["items"][0]
        create_item(appstruct, self.request, proxy)

        update = {"id": appstruct["id"],
                  "title": {"default": u"New unique_name"}}
        webshop_id = proxy.update([update])[0]
        results = proxy.single_call('catalog_product.info', [webshop_id])
        assert results["name"] == u"New unique_name"

    def test_magentoapi_items_update_shops(self):
        proxy = self.items_proxy
        appstruct = {"id": u"item", "sku": u"itemsku",
                     "shops": [("ch_hobby", True),  # items visible
                               ("ch_profi", False),  # items not visible
                               ("fr_profi", True),  # items visible
                               ("de_resell", False),  # items not visible
                               ],
                     "title": {"default": u"default title", "fr": u"fr title"},
                     "price": [("ch_website", 2.0),
                               ("fr_website", 3.0),
                               ("de_website", 1.0),
                               ]
                     }
        item = create_item(appstruct, self.request, proxy)

        proxy.update_shops([item.webshop_id], [appstruct])
        fr_ch_hobby = proxy.single_call('catalog_product.info',
                                        [item.webshop_id, "fr_ch_hobby"])
        assert fr_ch_hobby["name"] == "fr title"
        assert fr_ch_hobby["visibility"] == "4"
        assert fr_ch_hobby["price"] == "2.0000"
        de_ch_hobby = proxy.single_call('catalog_product.info',
                                        [item.webshop_id, "de_ch_hobby"])
        assert de_ch_hobby["name"] == "default title"
        assert de_ch_hobby["visibility"] == "4"
        assert de_ch_hobby["price"] == "2.0000"
        it_ch_hobby = proxy.single_call('catalog_product.info',
                                        [item.webshop_id, "it_ch_hobby"])
        assert it_ch_hobby["name"] == "default title"
        assert it_ch_hobby["visibility"] == "4"
        assert it_ch_hobby["price"] == "2.0000"
        de_ch_profi = proxy.single_call('catalog_product.info',
                                        [item.webshop_id, "de_ch_profi"])
        assert de_ch_profi["name"] == "default title"
        assert de_ch_profi["visibility"] == "1"  # item not visible
        assert de_ch_profi["price"] == "2.0000"
        fr_fr_profi = proxy.single_call('catalog_product.info',
                                        [item.webshop_id, "fr_fr_profi"])
        assert fr_fr_profi["name"] == "fr title"
        assert fr_fr_profi["visibility"] == "4"
        assert fr_fr_profi["price"] == "3.0000"
        fr_fr_hobby = proxy.single_call('catalog_product.info',
                                        [item.webshop_id, "fr_fr_hobby"])
        assert fr_fr_hobby["visibility"] == "1"  # item not visible
        de_de_hobby = proxy.single_call('catalog_product.info',
                                        [item.webshop_id, "de_de_hobby"])
        assert de_de_hobby["price"] == "1.0000"
        assert de_de_hobby["visibility"] == "1"  # item not visible

    def test_magentoapi_delete_items(self):
        proxy = self.items_proxy
        appstruct = self.testdata["items"][0]
        item = create_item(appstruct, self.request, proxy)

        results = proxy.delete([item.webshop_id])
        assert results == [item.webshop_id]
        products = proxy.single_call('catalog_product.list')
        assert products == []
        results = proxy.delete(["wrongid"])
        assert results == ["wrongid"]


class TestMagentoAPIItemGroupsIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")
    items_proxy_class = magentoapi.ItemGroups

    def test_magentoapi_create_item_groups(self):
        proxy = self.item_groups_proxy
        appstruct = self.testdata["item_groups"][0]
        appstruct["title"]["default"] = u"unique_name"
        webshop_id = proxy.create([appstruct])[0]
        assert webshop_id > 0

    def test_magentoapi_update_item_groups(self):
        proxy = self.item_groups_proxy
        appstruct = self.testdata["item_groups"][0]
        appstruct = self.testdata["item_groups"][0]
        appstruct["title"]["default"] = u"unique_name"
        create_item_group(appstruct, self.request, proxy)

        update = {"id": appstruct["id"],
                  "title": {"default": u"New unique_name"}}
        webshop_id = proxy.update([update])[0]
        results = proxy.single_call('catalog_product.info', [webshop_id])
        assert results["name"] == u"New unique_name"

    def test_magentoapi_delete_item_groups(self):
        proxy = self.item_groups_proxy
        appstruct = self.testdata["item_groups"][0]
        item_group = create_item_group(appstruct, self.request, proxy)

        results = proxy.delete([item_group.webshop_id])
        assert results == [True]


class TestMagentoAPICategoriesIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")

    def test_magentoapi_categories_to_create_data(self):
        appstruct = {}
        data = self.categories_proxy._to_create_data(appstruct)
        default_data = {"available_sort_by": ["position", "name", "price"],
                        "default_sort_by": "position",
                        "include_in_menu": 1,
                        "is_active": 0}
        assert data == default_data

    def test_magentoapi_categories_create(self):
        proxy = self.categories_proxy
        appstruct = self.testdata["categories"][0]
        webshop_id = proxy.create([appstruct])[0]
        default_children = proxy.single_call("catalog_category.level",
                                             [None, None, 2])
        assert webshop_id == int(default_children[0]["category_id"])

    def test_magentoapi_categories_link_category_parents(self):
        proxy = self.categories_proxy
        appstruct_p = {"id": u"parent", "parent_id": None, "title": {"default":
                                                                     "parent"}}
        appstruct_c = {"id": u"child", "parent_id": u"parent", "title":
                       {"default": "child"}}
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

    def test_magentoapi_categories_update_categories(self):
        proxy = self.categories_proxy
        appstruct = self.testdata["categories"][0]
        appstruct["title"]["default"] = u"unique_name"
        create_category(appstruct, self.request, proxy)

        update = {"id": appstruct["id"],
                  "title": {"default": u"New unique_name"}}
        webshop_id = proxy.update([update])[0]
        results = proxy.single_call('catalog_category.info', [webshop_id])
        assert results["name"] == u"New unique_name"

    def test_magentoapi_categories_delete_categories(self):
        proxy = self.categories_proxy
        appstruct = self.testdata["categories"][0]
        category = create_category(appstruct, self.request, proxy)

        results = proxy.delete([category.webshop_id])
        assert results == [True]


# -*- coding: utf-8 -*-
from decimal import Decimal
import pytest
import unittest
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    MagentoIntegrationTestCase,
    MagentoTestdatabaseIntegrationTestCase,
    create_item,
    create_category,
    create_item_group,
)
from organicseeds_webshop_api import magentoapi


class TestMagentoAPIHelpersIntegration(IntegrationTestCase):

    def test_indexing_reindex(self):
        from organicseeds_webshop_api import magentoapi
        result = magentoapi.indexing_reindex(self.request)
        assert "Reindexing" in result

    def test_indexing_enable_manual(self):
        from organicseeds_webshop_api import magentoapi
        result = magentoapi.indexing_enable_manual(self.request)
        assert "Manual" in result

    def test_indexing_enable_auto(self):
        from organicseeds_webshop_api import magentoapi
        result = magentoapi.indexing_enable_auto(self.request)
        assert "Update on Save" in result


class TestMagentoCatalogAPIHelpersIntegration(unittest.TestCase):

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

    def test_magentoapi_get_all_website_ids(self):
        from organicseeds_webshop_api import magentoapi
        websites = magentoapi.get_all_website_ids()
        assert websites == ["ch_website", "de_website", "fr_website"]

    def test_magentoapi_get_tier_price_data(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"tierprices": [{"website": "de_website",
                                     "customer_group_id": 0,
                                     "qty": 100,
                                     "price": 4.20}]}
        data = magentoapi.get_tier_price_data(appstruct)
        assert data == [{'customer_group_id': 0, 'website': 'de_website',
                         'qty': 100, 'price': 4.20}]
        appstruct = {}
        data = magentoapi.get_tier_price_data(appstruct)
        assert data is None

    def test_magentoapi_get_stock_data_none(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {}
        data = magentoapi.get_stock_data(appstruct)
        assert data is None

    def test_magentoapi_get_stock_data_is_in_stock(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"inventory_status": 2, "inventory_qty": 300}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'qty': 300, 'is_in_stock': 1}

        appstruct = {"inventory_status": 7, "inventory_qty": 300}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'qty': 300, 'is_in_stock': 1}

        appstruct = {"inventory_status": 8, "inventory_qty": 300}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'qty': 300, 'is_in_stock': 1}

    def test_magentoapi_get_stock_data_is_not_in_stock(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"inventory_status": 3, "inventory_qty": -3}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'qty': -3, 'is_in_stock': 0}
        appstruct = {"inventory_status": 1, "inventory_qty": -3}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'qty': -3, 'is_in_stock': 0}

    def test_magentoapi_get_stock_data_min_sale(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"min_sale_qty": 5}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'use_config_min_sale_qty': 0, 'min_sale_qty': 5}

    def test_magentoapi_get_stock_data_max_sale(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"max_sale_qty": 1000}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'use_config_max_sale_qty': 0, 'max_sale_qty': 1000}

    def test_magentoapi_get_stock_data_qty_increments(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"inventory_qty_increments": 5}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'use_config_enable_qty_inc': 0,
                        'use_config_qty_increments': 0,
                        'enable_qty_increments': 1, 'qty_increments': 5}

    def test_magentoapi_get_stock_data_backorders_enable(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"backorders_allow": True}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'use_config_backorders': 0, "backorders": 2,
                        "min_qty": -10000000}

    def test_magentoapi_get_stock_data_backorders_disable(self):
        from organicseeds_webshop_api import magentoapi
        appstruct = {"backorders_allow": False}
        data = magentoapi.get_stock_data(appstruct)
        assert data == {'use_config_backorders': 0, "backorders": 0,
                        "min_qty": 0}


class TestMagentoSalesAPIHelpersIntegration(unittest.TestCase):

    def test_order_data_to_appstruct(self):
        order_data = TESTDATA_ORDER_GUEST_CUSTOMER
        from organicseeds_webshop_api.magentoapi import order_data_to_appstruct
        order = order_data_to_appstruct(order_data)
        assert order == TESTDATA_ORDER_GUEST_CUSTOMER_EXPECTED


class TestMagentoAPIIntegration(MagentoIntegrationTestCase):

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
                        'url_key': u'titlefr-itemka32-fr',
                        'price': 2.0}
        data = proxy._to_update_shops_data(appstruct, "default", "default")
        assert data == {'name': 'title',
                        'short_description': 'kurzbeschreibung',
                        'url_key': u'title-itemka32',
                        'description': 'Ausfuehrliche Beschreibung'
                        }

    def test_magentoapi_items_to_update_data(self):
        appstruct = self.testdata["items"][0]
        data = self.items_proxy._to_update_data(appstruct)
        assert ('weight', 0.25) in data.items()
        assert ('url_key', u'title-itemka32') in data.items()
        assert ('tier_price', [{'customer_group_id': 0,
                                'website': 'de_website',
                                'qty': 100, 'price': 4.20}]) in data.items()
        assert data['additional_attributes'] == \
            {'single_data': {'webshopapi_type': 'sortendetail_default_vpe',
                             'webshopapi_id': 'itemka32'}}
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
        assert result["websites"] == ['2', '3', '4']
        assert result["price"] is None
        assert result["status"] == '1'
        assert len(result["tier_price"]) == 1
        assert result['webshopapi_id'] == appstruct["id"]
        assert result['webshopapi_type'] == appstruct["__type__"]
        result = proxy.single_call("cataloginventory_stock_item.list",
                                   [webshop_id])[0]
        assert result['is_in_stock'] == '1'
        assert result['qty'] == '5.0000'

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
        assert results == [item_group.webshop_id]


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

    def test_magentoapi_items_to_update_data(self):
        appstruct = self.testdata["categories"][0]
        data = self.categories_proxy._to_update_data(appstruct)
        assert data['additional_attributes'] ==\
            {'single_data': {'webshopapi_type': 'category',
                             'webshopapi_id': 1000}}
        appstruct = {}
        data = self.categories_proxy._to_update_data(appstruct)
        assert data == {}

    def test_magentoapi_categories_create(self):
        proxy = self.categories_proxy
        appstruct = self.testdata["categories"][0]
        webshop_id = proxy.create([appstruct])[0]
        default_children = proxy.single_call("catalog_category.level",
                                             [None, None, 2])
        assert webshop_id == int(default_children[0]["category_id"])

    def test_magentoapi_categories_update_shops(self):
        proxy = self.categories_proxy
        appstruct = {"id": u"cat1",
                     "shops": [("ch_hobby", True),  # visible
                               ("ch_profi", False),  # not visible
                               ("fr_profi", True),  # visible
                               ("de_resell", False),  # not visible
                               ],
                     "title": {"default": u"default title", "fr": u"fr title"},
                     }
        category = create_category(appstruct, self.request, proxy)

        proxy.update_shops([category.webshop_id], [appstruct])
        fr_ch_hobby = proxy.single_call('catalog_category.info',
                                        [category.webshop_id, "fr_ch_hobby"])
        assert fr_ch_hobby["name"] == "fr title"
        assert fr_ch_hobby["is_active"] == "1"
        de_ch_hobby = proxy.single_call('catalog_category.info',
                                        [category.webshop_id, "de_ch_hobby"])
        assert de_ch_hobby["name"] == "default title"
        assert de_ch_hobby["is_active"] == "1"
        it_ch_hobby = proxy.single_call('catalog_category.info',
                                        [category.webshop_id, "it_ch_hobby"])
        assert it_ch_hobby["name"] == "default title"
        assert it_ch_hobby["is_active"] == "1"
        de_ch_profi = proxy.single_call('catalog_category.info',
                                        [category.webshop_id, "de_ch_profi"])
        assert de_ch_profi["name"] == "default title"
        assert de_ch_profi["is_active"] == "0"  # category not visible
        fr_fr_profi = proxy.single_call('catalog_category.info',
                                        [category.webshop_id, "fr_fr_profi"])
        assert fr_fr_profi["name"] == "fr title"
        assert fr_fr_profi["is_active"] == "1"
        fr_fr_hobby = proxy.single_call('catalog_category.info',
                                        [category.webshop_id, "fr_fr_hobby"])
        assert fr_fr_hobby["is_active"] == "0"  # category not visible
        de_de_hobby = proxy.single_call('catalog_category.info',
                                        [category.webshop_id, "de_de_hobby"])
        assert de_de_hobby["is_active"] == "0"  # category not visible

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
        root = proxy.single_call("catalog_category.info",
                                 [category_p.webshop_id])
        assert root["is_anchor"] == '1'
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
        assert results == [category.webshop_id]


class TestMagentoAPISalesOrderUnit(MagentoTestdatabaseIntegrationTestCase):

    def test_magentoapi_salesorders_add_comment(self):
        increment_id = 200000001
        result = self.salesorders_proxy.add_comment(increment_id, "pending")
        assert result


TESTDATA_ORDER_GUEST_CUSTOMER = \
    {"adjustment_negative": None,
     "adjustment_positive": None,
     "applied_rule_ids": None,
     "base_adjustment_negative": None,
     "base_adjustment_positive": None,
     "base_currency_code": "CHF",
     "base_discount_amount": "0.0000",
     "base_discount_canceled": None,
     "base_discount_invoiced": None,
     "base_discount_refunded": None,
     "base_grand_total": "71.8000",
     "base_hidden_tax_amount": "0.0000",
     "base_hidden_tax_invoiced": None,
     "base_hidden_tax_refunded": None,
     "base_shipping_amount": "50.0000",
     "base_shipping_canceled": None,
     "base_shipping_discount_amount": "0.0000",
     "base_shipping_hidden_tax_amnt": "0.0000",
     "base_shipping_hidden_tax_amount": "0.0000",
     "base_shipping_incl_tax": "50.0000",
     "base_shipping_invoiced": None,
     "base_shipping_refunded": None,
     "base_shipping_tax_amount": "0.0000",
     "base_shipping_tax_refunded": None,
     "base_subtotal": "20.0000",
     "base_subtotal_canceled": None,
     "base_subtotal_incl_tax": "21.8000",
     "base_subtotal_invoiced": None,
     "base_subtotal_refunded": None,
     "base_tax_amount": "1.8000",
     "base_tax_canceled": None,
     "base_tax_invoiced": None,
     "base_tax_refunded": None,
     "base_to_global_rate": "1.0000",
     "base_to_order_rate": "1.0000",
     "base_total_canceled": None,
     "base_total_due": "71.8000",
     "base_total_invoiced": None,
     "base_total_invoiced_cost": None,
     "base_total_offline_refunded": None,
     "base_total_online_refunded": None,
     "base_total_paid": None,
     "base_total_qty_ordered": None,
     "base_total_refunded": None,
     "billing_address": {"address_id": "7",
                         "address_type": "billing",
                         "city": u"Z\xfcrich",
                         "company": "Company",
                         "country_id": "CH",
                         "customer_address_id": None,
                         "customer_id": None,
                         "email": "joka@developlocal.sativa.jokasis.de",
                         "fax": "123213213",
                         "firstname": "Joscha",
                         "lastname": "Krutzki",
                         "middlename": None,
                         "parent_id": "4",
                         "postcode": "12233",
                         "prefix": None,
                         "quote_address_id": None,
                         "region": "Aargau",
                         "region_id": "104",
                         "street": "Strasse1\nStrasse2",
                         "suffix": None,
                         "telephone": "030123213213",
                         "vat_id": None,
                         "vat_is_valid": None,
                         "vat_request_date": None,
                         "vat_request_id": None,
                         "vat_request_success": None},
     "billing_address_id": "7",
     "can_ship_partially": None,
     "can_ship_partially_item": None,
     "coupon_code": None,
     "coupon_rule_name": None,
     "created_at": "2013-05-14 12:29:03",
     "customer_dob": None,
     "customer_email": "joka@developlocal.sativa.jokasis.de",
     "customer_firstname": "Joscha",
     "customer_gender": None,
     "customer_group_id": "0",
     "customer_id": None,
     "customer_is_guest": "1",
     "customer_lastname": "Krutzki",
     "customer_middlename": None,
     "customer_note": None,
     "customer_note_notify": "1",
     "customer_prefix": None,
     "customer_suffix": None,
     "customer_taxvat": None,
     "discount_amount": "0.0000",
     "discount_canceled": None,
     "discount_description": None,
     "discount_invoiced": None,
     "discount_refunded": None,
     "edit_increment": None,
     "email_sent": "1",
     "ext_customer_id": None,
     "ext_order_id": None,
     "forced_do_shipment_with_invoice": None,
     "forced_shipment_with_invoice": None,
     "gift_message_id": None,
     "global_currency_code": "CHF",
     "grand_total": "71.8000",
     "hidden_tax_amount": "0.0000",
     "hidden_tax_invoiced": None,
     "hidden_tax_refunded": None,
     "hold_before_state": None,
     "hold_before_status": None,
     "increment_id": "200000004",
     "is_virtual": "0",
     "items": [{"additional_data": None,
                "amount_refunded": "0.0000",
                'applied_rule_ids': None,
                'base_amount_refunded': '0.0000',
                'base_cost': None,
                'base_discount_amount': '0.0000',
                'base_discount_invoiced': '0.0000',
                'base_discount_refunded': None,
                'base_hidden_tax_amount': None,
                'base_hidden_tax_invoiced': None,
                'base_hidden_tax_refunded': None,
                'base_original_price': '2.0000',
                'base_price': '2.0000',
                'base_price_incl_tax': '2.1800',
                'base_row_invoiced': '0.0000',
                'base_row_total': '20.0000',
                'base_row_total_incl_tax': '21.8000',
                'base_tax_amount': '1.8000',
                'base_tax_before_discount': None,
                'base_tax_invoiced': '0.0000',
                'base_tax_refunded': None,
                'base_weee_tax_applied_amount': '0.0000',
                'base_weee_tax_applied_row_amnt': '0.0000',
                'base_weee_tax_applied_row_amount': '0.0000',
                'base_weee_tax_disposition': '0.0000',
                'base_weee_tax_row_disposition': '0.0000',
                'created_at': '2013-05-14 12:29:03',
                'description': None,
                'discount_amount': '0.0000',
                'discount_invoiced': '0.0000',
                'discount_percent': '0.0000',
                'discount_refunded': None,
                'ext_order_item_id': None,
                'free_shipping': '0',
                'gift_message_available': None,
                'gift_message_id': None,
                'hidden_tax_amount': None,
                'hidden_tax_canceled': None,
                'hidden_tax_invoiced': None,
                'hidden_tax_refunded': None,
                'is_nominal': '0',
                'is_qty_decimal': '0',
                'is_virtual': '0',
                'item_id': '4',
                'locked_do_invoice': None,
                'locked_do_ship': None,
                'name': 'titlede',
                'no_discount': '0',
                'order_id': '4',
                'original_price': '2.0000',
                'parent_item_id': None,
                'price': '2.0000',
                'price_incl_tax': '2.1800',
                'product_id': '4',
                'product_options': '',
                'product_type': 'simple',
                'qty_backordered': None,
                'qty_canceled': '0.0000',
                'qty_invoiced': '0.0000',
                'qty_ordered': '10.0000',
                'qty_refunded': '0.0000',
                'qty_shipped': '0.0000',
                'quote_item_id': '2',
                'row_invoiced': '0.0000',
                'row_total': '20.0000',
                'row_total_incl_tax': '21.8000',
                'row_weight': '2.5000',
                'sku': 'itemka32',
                'store_id': '2',
                'tax_amount': '1.8000',
                'tax_before_discount': None,
                'tax_canceled': None,
                'tax_invoiced': '0.0000',
                'tax_percent': '9.0000',
                'tax_refunded': None,
                'updated_at': '2013-05-14 13:11:29',
                'weee_tax_applied': 'a:0:{}',
                'weee_tax_applied_amount': '0.0000',
                'weee_tax_applied_row_amount': '0.0000',
                'weee_tax_disposition': '0.0000',
                'weee_tax_row_disposition': '0.0000',
                'weight': '0.2500'}],
     'order_currency_code': 'CHF',
     'order_id': '4',
     'original_increment_id': None,
     'payment': {'account_status': None,
                 'additional_data': None,
                 'additional_information': [],
                 'address_status': None,
                 'amount_authorized': None,
                 'amount_canceled': None,
                 'amount_ordered': '71.8000',
                 'amount_paid': None,
                 'amount_refunded': None,
                 'anet_trans_method': None,
                 'base_amount_authorized': None,
                 'base_amount_canceled': None,
                 'base_amount_ordered': '71.8000',
                 'base_amount_paid': None,
                 'base_amount_paid_online': None,
                 'base_amount_refunded': None,
                 'base_amount_refunded_online': None,
                 'base_shipping_amount': '50.0000',
                 'base_shipping_captured': None,
                 'base_shipping_refunded': None,
                 'cc_approval': None,
                 'cc_avs_status': None,
                 'cc_cid_status': None,
                 'cc_debug_request_body': None,
                 'cc_debug_response_body': None,
                 'cc_debug_response_serialized': None,
                 'cc_exp_month': '0',
                 'cc_exp_year': '0',
                 'cc_last4': None,
                 'cc_number_enc': None,
                 'cc_owner': None,
                 'cc_secure_verify': None,
                 'cc_ss_issue': None,
                 'cc_ss_start_month': '0',
                 'cc_ss_start_year': '0',
                 'cc_status': None,
                 'cc_status_description': None,
                 'cc_trans_id': None,
                 'cc_type': None,
                 'echeck_account_name': None,
                 'echeck_account_type': None,
                 'echeck_bank_name': None,
                 'echeck_routing_number': None,
                 'echeck_type': None,
                 'last_trans_id': None,
                 'method': 'checkmo',
                 'parent_id': '4',
                 'paybox_request_number': None,
                 'payment_id': '4',
                 'payone_account_number': '0',
                 'payone_account_owner': '0',
                 'payone_bank_code': '0',
                 'payone_bank_country': '',
                 'payone_bank_group': '',
                 'payone_clearing_bank_account': '',
                 'payone_clearing_bank_accountholder': '',
                 'payone_clearing_bank_bic': '',
                 'payone_clearing_bank_city': '',
                 'payone_clearing_bank_code': '0',
                 'payone_clearing_bank_country': '',
                 'payone_clearing_bank_iban': '',
                 'payone_clearing_bank_name': '',
                 'payone_clearing_duedate': '',
                 'payone_clearing_instructionnote': '',
                 'payone_clearing_legalnote': '',
                 'payone_clearing_reference': '',
                 'payone_config_payment_method_id': '0',
                 'payone_financing_type': '',
                 'payone_onlinebanktransfer_type': '',
                 'payone_payment_method_name': '',
                 'payone_payment_method_type': '',
                 'payone_pseudocardpan': '',
                 'payone_safe_invoice_type': '',
                 'po_number': None,
                 'protection_eligibility': None,
                 'quote_payment_id': None,
                 'shipping_amount': '50.0000',
                 'shipping_captured': None,
                 'shipping_refunded': None},
     'payment_auth_expiration': None,
     'payment_authorization_amount': None,
     'payment_authorization_expiration': None,
     'payone_dunning_status': '',
     'payone_payment_method_type': '',
     'payone_transaction_status': '',
     'paypal_ipn_customer_notified': '0',
     'protect_code': 'b79803',
     'quote_address_id': None,
     'quote_id': '6',
     'relation_child_id': None,
     'relation_child_real_id': None,
     'relation_parent_id': None,
     'relation_parent_real_id': None,
     'remote_ip': '127.0.0.1',
     'shipping_address': {'address_id': '8',
                          'address_type': 'shipping',
                          'city': 'Arggau',
                          'company': 'VersandCompany',
                          'country_id': 'CH',
                          'customer_address_id': None,
                          'customer_id': None,
                          'email': None,
                          'fax': '123/213213213',
                          'firstname': 'VersandJosch',
                          'lastname': 'VersandKrutzki',
                          'middlename': None,
                          'parent_id': '4',
                          'postcode': '13333',
                          'prefix': None,
                          'quote_address_id': None,
                          'region': 'Appenzell Innerrhoden',
                          'region_id': '105',
                          'street': 'VersandAdresse1\nVersandAdresse2',
                          'suffix': None,
                          'telephone': '123333',
                          'vat_id': None,
                          'vat_is_valid': None,
                          'vat_request_date': None,
                          'vat_request_id': None,
                          'vat_request_success': None},
     'shipping_address_id': '8',
     'shipping_amount': '50.0000',
     'shipping_canceled': None,
     'shipping_description': 'Flat Rate - Fixed',
     'shipping_discount_amount': '0.0000',
     'shipping_hidden_tax_amount': '0.0000',
     'shipping_incl_tax': '50.0000',
     'shipping_invoiced': None,
     'shipping_method': 'flatrate_flatrate',
     'shipping_refunded': None,
     'shipping_tax_amount': '0.0000',
     'shipping_tax_refunded': None,
     'state': 'new',
     'status': 'pending',
     'status_history': [{'comment': None,
                         'created_at': '2013-05-14 13:11:29',
                         'entity_name': 'order',
                         'is_customer_notified': '2',
                         'is_visible_on_front': '0',
                         'parent_id': '4',
                         'status': 'pending',
                         'store_id': '2'},
                        {'comment': 'fdsfdsaf',
                         'created_at': '2013-05-14 12:50:03',
                         'entity_name': 'order',
                         'is_customer_notified': '1',
                         'is_visible_on_front': '0',
                         'parent_id': '4',
                         'status': 'holded',
                         'store_id': '2'},
                        {'comment': None,
                         'created_at': '2013-05-14 12:49:41',
                         'entity_name': 'order',
                         'is_customer_notified': '2',
                         'is_visible_on_front': '0',
                         'parent_id': '4',
                         'status': 'holded',
                         'store_id': '2'},
                        {'comment': None,
                         'created_at': '2013-05-14 12:29:03',
                         'entity_name': 'order',
                         'is_customer_notified': '1',
                         'is_visible_on_front': '0',
                         'parent_id': '4',
                         'status': 'pending',
                         'store_id': '2'}],
     'store_currency_code': 'CHF',
     'store_id': '2',
     'store_name': 'ch_website\nch_hobby\nDeutsch',
     'store_to_base_rate': '1.0000',
     'store_to_order_rate': '1.0000',
     'subtotal': '20.0000',
     'subtotal_canceled': None,
     'subtotal_incl_tax': '21.8000',
     'subtotal_invoiced': None,
     'subtotal_refunded': None,
     'tax_amount': '1.8000',
     'tax_canceled': None,
     'tax_invoiced': None,
     'tax_refunded': None,
     'total_canceled': None,
     'total_due': '71.8000',
     'total_invoiced': None,
     'total_item_count': '1',
     'total_offline_refunded': None,
     'total_online_refunded': None,
     'total_paid': None,
     'total_qty_ordered': '10.0000',
     'total_refunded': None,
     'updated_at': '2013-05-14 13:11:29',
     'weight': '2.5000',
     'x_forwarded_for': '127.0.0.1'}


TESTDATA_ORDER_GUEST_CUSTOMER_EXPECTED = \
    {'billing_address': {'city': u'Z\xfcrich',
                         'company': u'Company',
                         'country_id': u'CH',
                         'email': u'joka@developlocal.sativa.jokasis.de',
                         'fax': u'123213213',
                         'firstname': u'Joscha',
                         'lastname': u'Krutzki',
                         'postcode': u'12233',
                         'region': u'Aargau',
                         'street': u'Strasse1\nStrasse2',
                         'telephone': u'030123213213'},
     'coupon_code': u'',
     'coupon_rule_name': u'',
     'created_at': u'2013-05-14 12:29:03',
     'customer_dob': u'',
     'customer_email': u'joka@developlocal.sativa.jokasis.de',
     'customer_firstname': u'Joscha',
     'customer_gender': u'',
     'customer_group_id': 0,
     'customer_is_guest': True,
     'customer_lastname': u'Krutzki',
     'customer_prefix': u'',
     'customer_taxvat': u'',
     'discount_amount': Decimal('0.0000'),
     'discount_invoiced': Decimal('0'),
     'ext_customer_id': u'',
     'ext_order_id': u'',
     'grand_total': Decimal('71.8000'),
     'items': [{'discount_amount': Decimal('0.0000'),
                'discount_percent': Decimal('0.0000'),
                'free_shipping': False,
                'order_item_id': 4,
                'original_price': Decimal('2.0000'),
                'price': Decimal('2.0000'),
                'price_incl_tax': Decimal('2.1800'),
                'qty_backordered': Decimal('0'),
                'qty_invoice': Decimal('0'),
                'qty_ordered': Decimal('10.0000'),
                'qty_shipped': Decimal('0.0000'),
                'sku': u'itemka32',
                'tax_amount': Decimal('1.8000'),
                'tax_before_discount': Decimal('0'),
                'tax_invoiced': Decimal('0.0000'),
                'tax_percent': Decimal('9.0000'),
                'title': u'titlede',
                'weight': Decimal('0.2500')}],
     'order_currency_code': u'CHF',
     'order_increment_id': 1,
     'payment_id': 4,
     'payment_method': u'',
     'payone_account_number': 0,
     'payone_account_owner': 0,
     'payone_bank_code': 0,
     'payone_bank_country': u'',
     'payone_bank_group': u'',
     'payone_clearing_bank_account': u'',
     'payone_clearing_bank_accountholder': u'',
     'payone_clearing_bank_bic': u'',
     'payone_clearing_bank_city': u'',
     'payone_clearing_bank_code': 0,
     'payone_clearing_bank_country': u'',
     'payone_clearing_bank_iban': u'',
     'payone_clearing_bank_name': u'',
     'payone_clearing_duedate': u'',
     'payone_clearing_instructionnote': u'',
     'payone_clearing_legalnote': u'',
     'payone_clearing_reference': u'',
     'payone_config_payment_method_id': 0,
     'payone_dunning_status': u'',
     'payone_financing_type': u'',
     'payone_onlinebanktransfer_type': u'',
     'payone_payment_method_name': u'',
     'payone_payment_method_type': u'',
     'payone_pseudocardpan': u'',
     'payone_safe_invoice_type': u'',
     'payone_transaction_status': u'',
     'shipping_address': {'city': u'Arggau',
                          'company': u'VersandCompany',
                          'country_id': u'CH',
                          'email': u'',
                          'fax': u'123/213213213',
                          'firstname': u'VersandJosch',
                          'lastname': u'VersandKrutzki',
                          'postcode': u'13333',
                          'region': u'Appenzell Innerrhoden',
                          'street': u'VersandAdresse1\nVersandAdresse2',
                          'telephone': u'123333'},
     'shipping_amount': Decimal('50.0000'),
     'shipping_discount_amount': Decimal('0.0000'),
     'shipping_incl_tax': Decimal('50.0000'),
     'shipping_invoiced': Decimal('0'),
     'shipping_method': u'flatrate_flatrate',
     'shipping_tax_amount': Decimal('0.0000'),
     'shop': u'ch_hobby',
     'status': u'pending',
     'subtotal': Decimal('20.0000'),
     'subtotal_incl_tax': Decimal('21.8000'),
     'subtotal_invoiced': Decimal('0'),
     'tax_amount': Decimal('1.8000'),
     'tax_invoiced': Decimal('0'),
     'total_invoiced': Decimal('0'),
     'total_item_count': 1,
     'total_paid': Decimal('0'),
     'total_qty_ordered': Decimal('10.0000'),
     'updated_at': u'2013-05-14 13:11:29',
     'website': u'ch_website',
     'weight': 2.5}

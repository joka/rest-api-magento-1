import pytest

from organicseeds_webshop_api.exceptions import _400
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    MagentoIntegrationTestCase,
    MagentoTestdataIntegrationTestCase,
    create_all_testdata_items
)


class TestServicesCategoriesIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")

    def test_categories_post(self):
        from organicseeds_webshop_api.services import categories_post
        self.request.validated = self.testdata
        response = categories_post(self.request)
        assert(response == {'status': 'succeeded'})

    def test_categories_delete(self):
        from organicseeds_webshop_api.services import categories_delete
        from organicseeds_webshop_api.services import categories_post
        self.request.validated = self.testdata
        categories_post(self.request)
        response = categories_delete(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemGroupsIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_item_groups_post(self):
        from organicseeds_webshop_api.services import item_groups_post
        self.request.validated = self.testdata
        response = item_groups_post(self.request)
        assert(response == {'status': 'succeeded'})

    def test_item_groups_delete(self):
        from organicseeds_webshop_api.services import item_groups_delete
        from organicseeds_webshop_api.services import item_groups_post

        self.request.validated = self.testdata
        item_groups_post(self.request)
        response = item_groups_delete(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesVPETypesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/vpe_types_post.yaml")

    def test_vpe_types_post(self):
        from organicseeds_webshop_api.services import vpe_types_post
        self.request.validated = self.testdata
        response = vpe_types_post(self.request)
        assert(response == {'status': 'succeeded'})

    def test_vpe_types_put(self):
        from organicseeds_webshop_api.services import vpe_types_post
        from organicseeds_webshop_api.services import vpe_types_put
        self.request.validated = self.testdata
        response = vpe_types_post(self.request)
        response = vpe_types_put(self.request)
        assert(response == {'status': 'succeeded'})

    def test_vpe_type_delete(self):
        from organicseeds_webshop_api.services import vpe_types_delete
        from organicseeds_webshop_api.services import vpe_types_post

        self.request.validated = self.testdata
        vpe_types_post(self.request)
        response = vpe_types_delete(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesUnitOfMeasuresIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/unit_of_measures_post.yaml")

    def test_unit_of_measures_post(self):
        from organicseeds_webshop_api.services import unit_of_measures_post
        self.request.validated = self.testdata
        response = unit_of_measures_post(self.request)
        assert(response == {'status': 'succeeded'})

    def test_unit_of_measures_put(self):
        from organicseeds_webshop_api.services import unit_of_measures_post
        from organicseeds_webshop_api.services import unit_of_measures_put
        self.request.validated = self.testdata
        unit_of_measures_post(self.request)
        response = unit_of_measures_put(self.request)
        assert(response == {'status': 'succeeded'})

    def test_unit_of_measures_delete(self):
        from organicseeds_webshop_api.services import unit_of_measures_delete
        from organicseeds_webshop_api.services import unit_of_measures_post

        self.request.validated = self.testdata
        unit_of_measures_post(self.request)
        response = unit_of_measures_delete(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemsIntegration(MagentoIntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_items_post(self):
        from organicseeds_webshop_api.services import items_post
        self.request.validated = self.testdata
        response = items_post(self.request)
        assert(response == {'status': 'succeeded'})

    def test_items_delete(self):
        from organicseeds_webshop_api.services import items_delete
        from organicseeds_webshop_api.services import items_post

        self.request.validated = self.testdata
        response = items_post(self.request)
        response = items_delete(self.request)
        assert(response == {'status': 'succeeded'})

    def test_items_put(self):
        from organicseeds_webshop_api.services import items_post
        from organicseeds_webshop_api.services import items_put
        items = self.testdata
        self.request.validated = items
        items_post(self.request)

        itemsupdate = {"items": [{"id": "itemka32",
                       "description": {'default': u'New Description'},
                       "order": None}]}
        self.request.validated = itemsupdate
        response = items_put(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_item_get(self):
        from organicseeds_webshop_api.services import item_get
        vpe, unit, item, group = create_all_testdata_items(self.request)

        self.request.validated = {"id": item["id"], "lang": "default"}
        response = item_get(self.request)
        assert response["title"] == item["title"]["default"]
        assert response["vpe_type"] == vpe.to_data("default")
        assert response["unit_of_measure"] == unit.to_data("default")
        assert response["quality"] == group["qualities"][0]

    def test_item_get_missing(self):
        from organicseeds_webshop_api.services import item_get

        self.request.validated = {"id": "wrong_id", "lang": "default"}
        with pytest.raises(_400):
            item_get(self.request)


class TestServicesItemGroupIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_item_group_get(self):
        from organicseeds_webshop_api.testing import set_testfile
        from organicseeds_webshop_api.services import item_group_get
        from organicseeds_webshop_api import models
        from organicseeds_webshop_api import utils
        cattests = set_testfile("/testdata/categories_post.yaml")["testdata"]
        utils.store(cattests["categories"], models.Category,
                    "categories", self.request)
        item_groups = utils.store(self.testdata["item_groups"],
                                  models.ItemGroup, "item_groups",
                                  self.request)
        item_group = item_groups[0]

        self.request.validated = {"id": item_group["id"], "lang": "default",
                                  "with_children": False,
                                  "children_shop_id": ""}
        response = item_group_get(self.request)
        assert response["title"] == item_group["title"]["default"]

    def test_item_group_get_missing(self):
        from organicseeds_webshop_api.services import item_group_get

        self.request.validated = {"id": "wrong_id", "lang": "default",
                                  "with_children": False,
                                  "children_shop_id": ""}
        with pytest.raises(_400):
            item_group_get(self.request)


class TestServicesSalesOrdersIntegration(MagentoTestdataIntegrationTestCase):

    def test_orders_get(self):
        from organicseeds_webshop_api.services import orders_get
        self.request.validated = {"status": "pending"}
        response = orders_get(self.request)
        assert len(response["orders"]) > 1

    def test_orders_put(self):
        from organicseeds_webshop_api.services import orders_put
        appstruct = {"order_increment_id": 200000001,
                     "status": "processing",
                     "comment": "Ihre Bestellung wird jetzt bearbeitet",
                     "notify": True,
                     }
        self.request.validated = {"orders": [appstruct]}
        response = orders_put(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesSalesInvoicesIntegration(MagentoTestdataIntegrationTestCase):

    def test_invoices_put_no_capture(self):
        from organicseeds_webshop_api.services import invoices_put
        appstruct = {"order_increment_id": 200000001,
                     "order_item_qtys": [{"order_item_id": 1,
                                          "qty": 1.0}],
                     "capture_online_payment": False,
                     "comment": "Custom Note",
                     "notify": True,
                     }
        self.request.validated = {"invoices": [appstruct]}
        result = invoices_put(self.request)
        assert result == {'invoice_results': [{'capture_error': u'',
                          'capture_status': u'no_capture',
                          'invoice_increment_id': 200000001,
                          'order_increment_id': 200000001}]
                          }

        result = self.salesorders_proxy.single_call("sales_order.info",
                                                    [200000001])
        assert result["status"] == "processing"


class TestServicesSearchIntegration(IntegrationTestCase):

    def test_search_item_or_groups(self):
        from organicseeds_webshop_api.services import search_get
        self.request.GET = {}
        self.request.validated = {"lang": "default", "operator": "AND"}
        response = search_get(self.request)
        assert response == []

import pytest

from organicseeds_webshop_api.exceptions import _500
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    MagentoIntegrationTestCase,
    create_vpe_type,
    create_unit_of_measure,
    create_item_group,
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
        from organicseeds_webshop_api.testing import set_testfile
        from organicseeds_webshop_api.services import item_get
        from organicseeds_webshop_api import models
        from organicseeds_webshop_api import utils
        vpes = set_testfile("/testdata/vpe_types_post.yaml")["testdata"]
        vpe_appstruct = vpes["vpe_types"][0]
        vpe = create_vpe_type(vpe_appstruct, self.request)
        units = set_testfile("/testdata/unit_of_measures_post.yaml")["testdata"]
        unit_appstruct = units["unit_of_measures"][0]
        unit = create_unit_of_measure(unit_appstruct, self.request)
        item_groups = set_testfile("/testdata/item_groups_post.yaml")["testdata"]
        item_group_appstruct = item_groups["item_groups"][0]
        item_group = create_item_group(item_group_appstruct, self.request)
        items = utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = items[0]

        self.request.validated = {"id": item["id"], "lang": "default"}
        response = item_get(self.request)
        assert response["title"] == item["title"]["default"]
        assert response["vpe_type"] == vpe.to_data("default")
        assert response["unit_of_measure"] == unit.to_data("default")
        assert response["quality"] == item_group["qualities"][0]
        assert response["webshop_id"] == item_group.webshop_id

    def test_item_get_missing(self):
        from organicseeds_webshop_api.services import item_get

        self.request.validated = {"id": "wrong_id", "lang": "default"}
        with pytest.raises(_500):
            item_get(self.request)


class TestServicesItemGroupIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_item_group_get(self):
        from organicseeds_webshop_api.testing import set_testfile
        from organicseeds_webshop_api.services import item_group_get
        from organicseeds_webshop_api import models
        from organicseeds_webshop_api import utils
        categories_appstructs = set_testfile("/testdata/categories_post.yaml")["testdata"]
        categories = utils.store(categories_appstructs["categories"], models.Category,
                                 "categories", self.request)
        category = categories[0]
        item_groups = utils.store(self.testdata["item_groups"], models.ItemGroup, "item_groups", self.request)
        item_group = item_groups[0]

        self.request.validated = {"id": item_group["id"], "lang": "default"}
        response = item_group_get(self.request)
        assert response["title"] == item_group["title"]["default"]

    def test_item_group_get_missing(self):
        from organicseeds_webshop_api.services import item_group_get

        self.request.validated = {"id": "wrong_id", "lang": "default"}
        with pytest.raises(_500):
            item_group_get(self.request)

import pytest

from organicseeds_webshop_api.exceptions import _500
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    MagentoIntegrationTestCase
)


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
        assert response["description"] == item["description"]["default"]
        assert response["short_description"] == item["short_description"]["default"]
        assert response["vpe_type"] == vpe.to_data("default")
        assert response["unit_of_measure"] == unit.to_data("default")
        assert response["quality"] == item_group["qualities"][0]

    def test_item_get_missing(self):
        from organicseeds_webshop_api.services import item_get

        self.request.validated = {"id": "wrong_id", "lang": "default"}
        with pytest.raises(_500):
            item_get(self.request)

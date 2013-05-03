from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
)


class TestUtilsCategoriesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")

    def test_utils_remove_none_values(self):
        from organicseeds_webshop_api import utils
        appstructs = [{"key1": "value", "key2": None}]
        filtered = utils.remove_none_values(appstructs)
        assert filtered == [{"key1": "value"}]

    def test_utils_store_categories(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        from repoze.catalog.query import Eq

        categories = utils.store(self.testdata["categories"], models.Category,
                                 "categories", self.request)
        assert len(categories) == 5
        assert len(self.app_root["categories"]) == 5
        catalog = self.app_root["catalog"]
        search1 = catalog.query(Eq('__type__', 'category'))[0]
        search2 = catalog.query(Eq('__type__', 'sortenuebersicht'))[0]
        assert(search1 + search2 == 5)

    def test_utils_delete_categories(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        from repoze.catalog.query import Eq
        utils.store(self.testdata["categories"], models.Category,
                    "categories", self.request)

        utils.delete(self.testdata["categories"], "categories", self.request)
        categories = [x for x in self.app_root["categories"].items()]
        assert(categories == [])
        catalog = self.app_root["catalog"]
        search1 = catalog.query(Eq('__type__', 'category'))[0]
        serach2 = catalog.query(Eq('__type__', 'sortenuebersicht'))[0]
        assert(search1 + serach2 == 0)

    def test_utils_store_categories_with_parents(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["categories"][1]["parent_id"] = 1000
        utils.store(self.testdata["categories"], models.Category,
                    "categories", self.request)
        root = self.app_root["categories"][1000]
        child = self.app_root["categories"][1001]
        assert root.__parent__ is None
        assert child.__parent__ is root

    def test_utils_store_categories_with_parents_missing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["categories"][1]["parent_id"] = "unknown"
        utils.store(self.testdata["categories"], models.Category,
                    "categories", self.request)
        root = self.app_root["categories"][1000]
        child = self.app_root["categories"][1001]
        assert root.__parent__ is None
        assert child.__parent__ is None

    def test_get_entities_item_children_none(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        category = models.Category()
        item_webshop_ids, items = utils.get_entities_item_children(
            [category], self.request)
        assert item_webshop_ids == items == []

    def test_get_entities_item_children(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        category = models.Category()
        category.from_appstruct({"id": "parent"})

        item = models.Item()
        item.from_appstruct({"id": "child1", "parent_id": "parent"})
        self.request.root.app_root["items"]["child"] = item
        item_group = models.ItemGroup()
        item_group.from_appstruct({"id": "child2", "parent_id": "parent"})
        self.request.root.app_root["item_groups"]["child"] = item_group

        item_webshop_ids, items = utils.get_entities_item_children(
            [category], self.request)
        assert item_webshop_ids == [0, 0]
        assert items == [item, item_group]


class TestUtilsItemGroupsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_utils_store_item_groups(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        groups = utils.store(self.testdata["item_groups"], models.ItemGroup,
                             "item_groups", self.request)
        assert len(groups) == 1

    def test_utils_delete_item_groups(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        utils.store(self.testdata["item_groups"], models.ItemGroup,
                    "item_groups", self.request)

        utils.delete(self.testdata["item_groups"], "item_groups", self.request)
        item_groups = [x for x in self.app_root["item_groups"].items()]
        assert(item_groups == [])


class TestUtilsVPETypesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/vpe_types_post.yaml")

    def test_utils_store_vpe_types(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        vpe_types = utils.store(self.testdata["vpe_types"], models.EntityData,
                                "vpe_types", self.request)
        assert len(vpe_types) == 1


class TestUtilsUnitOfMeasuresIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/unit_of_measures_post.yaml")

    def test_store_unit_of_measures(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        units = utils.store(self.testdata["unit_of_measures"],
                            models.EntityData,
                            "unit_of_measures", self.request)
        assert len(units) == 1


class TestUtilsItemsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_utils_store_items(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        from repoze.catalog.query import Eq
        catalog = self.app_root["catalog"]

        items = utils.store(self.testdata["items"], models.Item,
                            "items", self.request)
        assert len(items) == 1
        search_results = catalog.query(Eq('id', 'itemka32'))[0]
        assert(search_results == 1)

    def test_utils_delete_items(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        from repoze.catalog.query import Eq
        utils.store(self.testdata["items"], models.Item, "items", self.request)

        utils.delete(self.testdata["items"], "items", self.request)
        items = [x for x in self.app_root["items"].items()]
        assert(items == [])
        catalog = self.app_root["catalog"]
        search_results = catalog.query(Eq('id', 'itemka32'))[0]
        assert(search_results == 0)

    def test_utils_store_items_with_parent(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["items"][0]["parent_id"] = "karotten"
        self.testdata["items"][0]["id"] = "itemka32"
        parent = object()
        self.app_root["item_groups"]["karotten"] = parent

        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.__parent__ is parent

    def test_utils_store_items_with_parent_missing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["items"][0]["parent_id"] = "unknown"
        self.testdata["items"][0]["id"] = "itemka32"

        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.__parent__ is None

    def test_utils_store_items_existing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models

        utils.store(self.testdata["items"], models.Item, "items", self.request)
        itemsupdate = {"items": [{"id": "itemka32",
                       "description": {'default': u'New Description'},
                       "order": None}]}
        utils.store(itemsupdate["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item["description"] == {'default': u'New Description'}
        assert item["order"] is None

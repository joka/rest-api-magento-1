# -*- coding: utf-8 -*-
import unittest
import pytest
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
)


class TestUtilsStoreEntitiesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_utils_store_entities(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        from repoze.catalog.query import Eq
        catalog = self.app_root["catalog"]
        self.testdata["items"][0]["title"] = {"default": "Aktuelle Aussaten"}

        items = utils.store(self.testdata["items"], models.Item,
                            "items", self.request)
        assert len(items) == len(self.testdata["items"])
        results = catalog.query(Eq('id', 'itemka32'))[0]
        assert(results == 1)

    def test_utils_store_entities_with_url_slug(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        from organicseeds_webshop_api.url_normalizer import url_normalizer
        from repoze.catalog.query import Eq
        catalog = self.app_root["catalog"]
        appstructs = [{"id": "1",
                       "sku": "sku1",
                       "title": {"default": "title", "fr": u"titlé fr"}}]
        item = utils.store(appstructs, models.Item, "items", self.request)[0]
        assert item["url_slug"]["default"] == url_normalizer('title' + "-1")
        assert item["url_slug"]["fr"] == url_normalizer(u'titlé fr') + "-1-fr"
        results = catalog.query(Eq('title_url_slugs',
                                   url_normalizer(u'titlé fr') + "-1-fr"))[0]
        assert(results == 1)

    def test_utils_store_entities_with_parent(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["items"][0]["parent_id"] = "karotten"
        self.testdata["items"][0]["id"] = "itemka32"
        parent = models.ItemGroup()
        self.app_root["item_groups"]["karotten"] = parent

        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.__parent__ is parent
        assert parent.__children__ == [item]

    def test_utils_store_entities_with_parent_missing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["items"][0]["parent_id"] = "wrong_id"
        self.testdata["items"][0]["id"] = "itemka32"
        parent = models.ItemGroup()
        self.app_root["item_groups"]["karotten"] = parent
        models.ItemGroup().__children__
        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.__parent__ is None
        assert parent.__children__ == []

    def test_utils_store_entities_update_parent(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["items"][0]["parent_id"] = "karotten"
        self.testdata["items"][0]["id"] = "itemka32"
        item = utils.store(self.testdata["items"], models.Item, "items",
                           self.request)[0]

        parent = utils.store([{"id": "karotten"}], models.ItemGroup,
                             "item_groups", self.request)[0]
        assert item.__parent__ is parent
        assert parent.__children__ == [item]

    def test_utils_store_entities_with_vpe_type(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["items"][0]["vpe_type_id"] = "portion"
        vpe_type = models.EntityData()
        self.app_root["vpe_types"]["portion"] = vpe_type

        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.vpe_type == vpe_type

    def test_utils_store_entities_with_vpe_type_missing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.vpe_type is None

    def test_utils_store_entities_with_unit_of_measure(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        self.testdata["items"][0]["unit_of_measure_id"] = "unit"
        unit = models.EntityData()
        self.app_root["unit_of_measures"]["unit"] = unit

        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.unit_of_measure == unit

    def test_utils_store_entities_with_unit_of_measure_missing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.unit_of_measure is None

    def test_utils_store_entities_with_quality(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        quality = {"id": "quality"}
        parent = models.ItemGroup()
        parent.from_appstruct({"qualities": [quality]})
        self.app_root["item_groups"]["parent"] = parent

        self.testdata["items"][0]["parent_id"] = "parent"
        self.testdata["items"][0]["quality_id"] = "quality"
        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.quality is quality

    def test_utils_store_entities_with_quality_parent_missing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        utils.store(self.testdata["items"], models.Item, "items", self.request)
        item = self.app_root["items"]["itemka32"]
        assert item.quality is None

    def test_utils_store_entities_with_quality_wrong_id(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        from organicseeds_webshop_api.exceptions import _400
        quality = {"id": "quality"}
        parent = models.ItemGroup()
        parent.from_appstruct({"qualities": [quality]})
        self.app_root["item_groups"]["parent"] = parent

        self.testdata["items"][0]["parent_id"] = "parent"
        self.testdata["items"][0]["wrong_quality_id"] = "quality"
        with pytest.raises(_400):
            utils.store(self.testdata["items"], models.Item, "items",
                        self.request)

    def test_utils_store_entities_update_item_quality(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        quality = {"id": "quality"}
        child_appstruct = {"id": "child", "parent_id": "parent",
                           "quality_id": "quality"}
        childs = utils.store([child_appstruct], models.Item, "items",
                             self.request)
        child = childs[0]
        utils.store([{"id": "parent", "qualities": [quality]}],
                    models.ItemGroup, "item_groups", self.request)
        assert child.quality is quality

    def test_utils_store_entities_update_item_quality_wrong_id(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        from organicseeds_webshop_api.exceptions import _400
        quality = {"id": "quality"}
        child_appstruct = {"id": "child", "parent_id": "parent",
                           "quality_id": "wrong_id"}
        utils.store([child_appstruct], models.Item, "items", self.request)

        with pytest.raises(_400):
            quality = {"id": "quality"}
            utils.store([{"id": "parent", "qualities": [quality]}],
                        models.ItemGroup, "item_groups", self.request)

    def test_utils_store_entities_update_item_quality_missing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        child = models.Item()
        child.from_appstruct({"id": "child",
                              "parent_id": "parent", "quality_id": "quality"})
        self.app_root["items"]["child"] = child

        utils.store([{"id": "parent", "qualities": []}],
                    models.ItemGroup, "item_groups", self.request)
        assert child.quality is None


class TestUtilsDeleteEntitiesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_utils_delete_entities(self):
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

    def test_utils_delete_entities_with_parents(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        item = utils.store(self.testdata["items"], models.Item, "items",
                           self.request)[0]
        parent = models.ItemGroup()
        item.__parent__ = parent
        parent.__children__.append(item)
        utils.delete(self.testdata["items"], "items", self.request)
        assert item.__parent__ is None
        assert item not in parent.__children__

    def test_utils_delete_entities_all(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        utils.store(self.testdata["items"], models.Item, "items",
                    self.request)
        utils.delete_all("items", self.request)
        items = [x for x in self.app_root["items"].items()]
        assert(items == [])


class TestUtilsRemoveNoneValues(unittest.TestCase):

    def test_utils_remove_none_values(self):
        from organicseeds_webshop_api import utils
        appstructs = [{"key1": "value", "key2": None}]
        filtered = utils.remove_none_values(appstructs)
        assert filtered == [{"key1": "value"}]


class TestUtilsGetEntitiesItemChildren(IntegrationTestCase):

    def test_get_entities_item_children(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        category = models.Category({"id": "parent"})
        item = models.Item({"id": "child1", "parent_id": "parent"})
        category.__children__.append(item)

        item_webshop_ids, items = utils.get_entities_item_children(
            [category], self.request)
        assert item_webshop_ids == [0]
        assert items == [item]

    def test_get_entities_item_children_missing(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        category = models.Category()
        item_webshop_ids, items = utils.get_entities_item_children(
            [category], self.request)
        assert item_webshop_ids == items == []


class TestUtilsGetUrl(IntegrationTestCase):

    def test_utils_get_url_slug(self):
        from organicseeds_webshop_api import utils
        appstruct = {"id": "cat1",
                     "title": {"default": u"testü.txt",
                               "fr": "titlé_fr",
                               "to_long": u"ddddddddddddddddddddddddddddddd"
                                          u"ddi ?dddddddddddddddddddddddddd"
                                          u"ddddddddddddddddddddddddddddddd"
                                          u"ddddddddddddddddddddddddddddddd"
                                          u"ddddddddddddddddddddddddddddddd"
                                          u"ddddddddddddddddddddddddddddddd"
                                          u"ddddddddddddddddddddddddddddddd"
                                          u"ddddddddddddddddddddddddddddddd"
                                          u"ddddddddddddddddddddddddddd.txt",
                               }}
        assert u'testu.txt-cat1' == utils.get_url_slug(appstruct, "default")
        assert u'newu-cat1' == utils.get_url_slug(appstruct, "wrong_lang")
        assert u'titla-c-_fr-cat1-fr' == utils.get_url_slug(appstruct, "fr")
        assert 34 == len(utils.get_url_slug(appstruct, "to_long"))


class TestUtilsSearch(IntegrationTestCase):

    def test_utils_search_missing_kwargs(self):
        from organicseeds_webshop_api import utils
        kwargs = {}
        results = utils.search(self.request, operator="AND", **kwargs)
        assert len(results) == 0

    def test_utils_search_AND(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        appstructs = [{"id": "item1",
                       "__type__": "vpe",
                       "title": {"default": "title"}},
                      {"id": "item2",
                       "__type__": "vpe",
                       "title": {"default": "title"}}
                      ]

        utils.store(appstructs, models.Item,
                    "items", self.request)
        kwargs = {"__type__": "vpe", "id": "item2"}
        results = utils.search(self.request, operator="AND", **kwargs)
        assert len(results) == 1
        kwargs = {"__type__": "vpe"}
        results = utils.search(self.request, operator="AND", **kwargs)
        assert len(results) == 2

    def test_utils_search_OR(self):
        from organicseeds_webshop_api import utils
        from organicseeds_webshop_api import models
        appstructs = [{"id": "item1",
                       "__type__": "vpe1",
                       "title": {"default": "title"}},
                      {"id": "item2",
                       "__type__": "vpe2",
                       "title": {"default": "title"}}
                      ]
        utils.store(appstructs, models.Item,
                    "items", self.request)
        kwargs = {"id": "item1", "__type__": "vpe2"}
        results = utils.search(self.request, operator="OR", **kwargs)
        assert len(results) == 2

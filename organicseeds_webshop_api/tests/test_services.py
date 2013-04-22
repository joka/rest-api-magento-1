from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
)


class TestServicesCategoriesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")

    def test_categories_post(self):
        from organicseeds_webshop_api.services import categories_post
        from repoze.catalog.query import Eq

        self.request.validated = self.testdata
        response = categories_post(self.request)
        assert(response == {'status': 'succeeded'})
        categories = [x for x in self.app_root["categories"].keys()]
        assert(len(categories) == 5)
        catalog = self.app_root["catalog"]
        search1 = catalog.query(Eq('__type__', 'category'))[0]
        search2 = catalog.query(Eq('__type__', 'sortenuebersicht'))[0]
        assert(search1 + search2 == 5)

    def test_categories_delete(self):
        from organicseeds_webshop_api.services import categories_delete
        from organicseeds_webshop_api.services import categories_post
        from repoze.catalog.query import Eq

        self.request.validated = self.testdata
        response = categories_post(self.request)

        self.request.validated = {}
        response = categories_delete(self.request)
        assert(response == {'status': 'succeeded'})
        categories = [x for x in self.app_root["categories"].items()]
        assert(categories == [])
        catalog = self.app_root["catalog"]
        search1 = catalog.query(Eq('__type__', 'category'))[0]
        serach2 = catalog.query(Eq('__type__', 'sortenuebersicht'))[0]
        assert(search1 + serach2 == 0)


class TestServicesItemGroupsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_item_groups_post(self):
        from organicseeds_webshop_api.services import item_groups_post
        self.request.validated = self.testdata
        response = item_groups_post(self.request)
        assert(response == {'status': 'succeeded'})
        item_groups = [x for x in self.app_root["item_groups"].items()]
        assert(len(item_groups) == 1)

    def test_item_groups_delete(self):
        from organicseeds_webshop_api.services import item_groups_delete
        from organicseeds_webshop_api.services import item_groups_post

        self.request.validated = self.testdata
        response = item_groups_post(self.request)

        self.request.validated = {}
        response = item_groups_delete(self.request)
        assert(response == {'status': 'succeeded'})
        item_groups = [x for x in self.app_root["item_groups"].items()]
        assert(item_groups == [])


class TestServicesVPETypesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/vpe_types_post.yaml")

    def test_vpe_types_post(self):
        from organicseeds_webshop_api.services import vpe_types_post
        self.request.validated = self.testdata
        response = vpe_types_post(self.request)
        assert(response == {'status': 'succeeded'})
        vpe_types = [x for x in self.app_root["vpe_types"].items()]
        assert(len(vpe_types) == 1)

    def test_vpe_type_delete(self):
        from organicseeds_webshop_api.services import vpe_types_delete
        from organicseeds_webshop_api.services import vpe_types_post

        self.request.validated = self.testdata
        response = vpe_types_post(self.request)

        self.request.validated = {}
        response = vpe_types_delete(self.request)
        assert(response == {'status': 'succeeded'})
        vpe_types = [x for x in self.app_root["vpe_types"].items()]
        assert(vpe_types == [])


class TestServicesUnitOfMeasuresIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/unit_of_measures_post.yaml")

    def test_unit_of_measures_post(self):
        from organicseeds_webshop_api.services import unit_of_measures_post
        self.request.validated = self.testdata
        response = unit_of_measures_post(self.request)
        assert(response == {'status': 'succeeded'})
        unit_of_measure = [x for x in
                           self.app_root["unit_of_measures"].items()]
        assert(len(unit_of_measure) == 1)

    def test_unit_of_measures_delete(self):
        from organicseeds_webshop_api.services import unit_of_measures_delete
        from organicseeds_webshop_api.services import unit_of_measures_post

        self.request.validated = self.testdata
        response = unit_of_measures_post(self.request)

        self.request.validated = {}
        response = unit_of_measures_delete(self.request)
        assert(response == {'status': 'succeeded'})
        unit_of_measure = [x for x in
                           self.app_root["unit_of_measures"].items()]
        assert(unit_of_measure == [])


class TestServicesItemsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_items_post(self):
        from organicseeds_webshop_api.services import items_post
        from repoze.catalog.query import Eq

        catalog = self.app_root["catalog"]
        self.request.validated = self.testdata
        response = items_post(self.request)
        assert(response == {'status': 'succeeded'})
        items = [x for x in self.app_root["items"].items()]
        assert(len(items) == 1)
        search_results = catalog.query(Eq('id', 'itemka32'))[0]
        assert(search_results == 1)

    def test_items_delete(self):
        from organicseeds_webshop_api.services import items_delete
        from organicseeds_webshop_api.services import items_post
        from repoze.catalog.query import Eq

        self.request.validated = self.testdata
        response = items_post(self.request)

        self.request.validated = {}
        response = items_delete(self.request)
        assert(response == {'status': 'succeeded'})
        items = [x for x in self.app_root["items"].items()]
        assert(items == [])
        catalog = self.app_root["catalog"]
        search_results = catalog.query(Eq('id', 'itemka32'))[0]
        assert(search_results == 0)

    def test_items_put(self):
        from organicseeds_webshop_api.services import items_post
        from organicseeds_webshop_api.services import items_put
        from repoze.catalog.query import Eq
        catalog = self.app_root["catalog"]
        items = self.testdata
        self.request.validated = items
        response = items_post(self.request)
        itemsupdate = self.testdata

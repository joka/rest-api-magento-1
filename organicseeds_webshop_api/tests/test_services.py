import json
import pytest
from webtest import AppError
from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    FunctionalTestCase,
    set_testfile,
)


class TestServicesCategoriesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")

    def test_post(self):
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

    def test_delete(self):
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

    def test_validator_parent_id_valid(self):
        from organicseeds_webshop_api.services import validate_category_parent_id
        self.request.validated = self.testdata
        validate_category_parent_id(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_parent_id_novalid_non_existent_id(self):
        from organicseeds_webshop_api.services import validate_category_parent_id
        self.testdata["categories"][0]['parent_id'] = u"non_existent"
        self.testdata["categories"][0]['id'] = u"1000"
        self.request.validated = self.testdata
        validate_category_parent_id(self.request)
        error_desription = 'parent_id: non_existent of category: 1000 does not'\
                           ' exists and is not going to be created'
        assert(error_desription == self.request.errors[0]["description"])

    def test_validator_parent_id_nonvalid_id_eq_parent_id(self):
        from organicseeds_webshop_api.services import validate_category_parent_id
        self.testdata["categories"][0]['parent_id'] = u"1000"
        self.testdata["categories"][0]['id'] = u"1000"
        self.request.validated = self.testdata
        validate_category_parent_id(self.request)
        error_desription = 'parent_id: 1000 and id: 1000 are the same'
        assert(error_desription == self.request.errors[0]["description"])

    def test_validator_id_nonvalid_already_exists(self):
        from organicseeds_webshop_api.services import validate_category_id
        self.testdata["categories"][0]['id'] = u"1000"
        existing = self.app_root["categories"]
        existing[u"1000"] = object()
        self.request.validated = self.testdata
        validate_category_id(self.request)
        error_desription = "The following ids do already exists"\
                           " in categories: [u'1000']"
        assert(error_desription == self.request.errors[0]["description"])
        del(existing[u"1000"])


class TestServicesItemGroupsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import item_groups_post
        self.request.validated = self.testdata
        response = item_groups_post(self.request)
        assert(response == {'status': 'succeeded'})
        item_groups = [x for x in self.app_root["item_groups"].items()]
        assert(len(item_groups) == 1)

    def test_delete(self):
        from organicseeds_webshop_api.services import item_groups_delete
        from organicseeds_webshop_api.services import item_groups_post

        self.request.validated = self.testdata
        response = item_groups_post(self.request)

        self.request.validated = {}
        response = item_groups_delete(self.request)
        assert(response == {'status': 'succeeded'})
        item_groups = [x for x in self.app_root["item_groups"].items()]
        assert(item_groups == [])

    def test_validator_no_item_references_exist_valid(self):
        from organicseeds_webshop_api.services import \
                validate_item_group_no_item_references_exist
        self.request.validated = self.testdata
        validate_item_group_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_no_item_references_exist_invalid(self):
        from organicseeds_webshop_api.services import \
                validate_item_group_no_item_references_exist
        self.request.validated = self.testdata
        self.app_root["item_groups"]["sortendetail"] = {}
        self.app_root["items"]["itemid"] = {}
        self.app_root["items"]["itemid"]["parent_id"] = u"sortendetail"
        validate_item_group_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 1)


class TestServicesVPETypesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/vpe_types_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import vpe_types_post
        self.request.validated = self.testdata
        response = vpe_types_post(self.request)
        assert(response == {'status': 'succeeded'})
        vpe_types = [x for x in self.app_root["vpe_types"].items()]
        assert(len(vpe_types) == 1)

    def test_delete(self):
        from organicseeds_webshop_api.services import vpe_types_delete
        from organicseeds_webshop_api.services import vpe_types_post

        self.request.validated = self.testdata
        response = vpe_types_post(self.request)

        self.request.validated = {}
        response = vpe_types_delete(self.request)
        assert(response == {'status': 'succeeded'})
        vpe_types = [x for x in self.app_root["vpe_types"].items()]
        assert(vpe_types == [])

    def test_validator_no_item_references_exist_valid(self):
        from organicseeds_webshop_api.services import \
                validate_vpe_type_no_item_references_exist
        self.request.validated = self.testdata
        validate_vpe_type_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_no_item_references_exist_invalid(self):
        from organicseeds_webshop_api.services import \
                validate_vpe_type_no_item_references_exist
        self.request.validated = self.testdata
        self.app_root["vpe_types"]["saatscheibe"] = {}
        self.app_root["items"]["itemid"] = {}
        self.app_root["items"]["itemid"]["vpe_type_id"] = u"saatscheibe"
        validate_vpe_type_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 1)


class TestServicesUnitOfMeasuresIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/unit_of_measures_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import unit_of_measures_post
        self.request.validated = self.testdata
        response = unit_of_measures_post(self.request)
        assert(response == {'status': 'succeeded'})
        unit_of_measure = [x for x in self.app_root["unit_of_measures"].items()]
        assert(len(unit_of_measure) == 1)

    def test_delete(self):
        from organicseeds_webshop_api.services import unit_of_measures_delete
        from organicseeds_webshop_api.services import unit_of_measures_post

        self.request.validated = self.testdata
        response = unit_of_measures_post(self.request)

        self.request.validated = {}
        response = unit_of_measures_delete(self.request)
        assert(response == {'status': 'succeeded'})
        unit_of_measure = [x for x in self.app_root["unit_of_measures"].items()]
        assert(unit_of_measure == [])

    def test_validator_no_item_references_exist_valid(self):
        from organicseeds_webshop_api.services import \
                validate_unit_of_measure_no_item_references_exist
        self.request.validated = self.testdata
        validate_unit_of_measure_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_no_item_references_exist_invalid(self):
        from organicseeds_webshop_api.services import \
                validate_unit_of_measure_no_item_references_exist
        self.request.validated = self.testdata
        self.app_root["unit_of_measures"]["portion"] = {}
        self.app_root["items"]["itemid"] = {}
        self.app_root["items"]["itemid"]["unit_of_measure_id"] = u"portion"
        validate_unit_of_measure_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 1)


class TestServicesItemsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_post(self):
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

    def test_delete(self):
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


class TestServicesFunctional(FunctionalTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_post_invalid(self):
        jsondata = self.testdata
        import ipdb; ipdb.set_trace()
        with pytest.raises(AppError):
            self.app.post_json('/items', jsondata)

    def test_post_valid(self):
        categories = set_testfile("/testdata/categories_post.yaml")["testdata"]
        resp = self.app.post_json('/categories', categories)
        assert resp.status_int == 200

        groups = set_testfile("/testdata/item_groups_post.yaml")["testdata"]
        resp = self.app.post_json('/item_groups', groups)
        assert resp.status_int == 200

        vpe = set_testfile("/testdata/vpe_types_post.yaml")["testdata"]
        resp = self.app.post_json('/vpe_types', vpe)
        assert resp.status_int == 200

        measure = set_testfile("/testdata/unit_of_measures_post.yaml")["testdata"]
        resp = self.app.post_json('/unit_of_measures', measure)
        assert resp.status_int == 200

        items = self.testdata
        resp = self.app.post_json('/items', items)
        assert resp.status_int == 200

    def test_delete_invalid(self):
        categories = set_testfile("/testdata/categories_post.yaml")["testdata"]
        self.app.post_json('/categories', categories)
        groups = set_testfile("/testdata/item_groups_post.yaml")["testdata"]
        self.app.post_json('/item_groups', groups)
        vpe = set_testfile("/testdata/vpe_types_post.yaml")["testdata"]
        self.app.post_json('/vpe_types', vpe)
        measure = set_testfile("/testdata/unit_of_measures_post.yaml")["testdata"]
        self.app.post_json('/unit_of_measures', measure)
        items = self.testdata
        self.app.post_json('/items', items)

        with pytest.raises(AppError):
            self.app.delete_json('/unit_of_measures', {})

    def test_delete_valid(self):
        categories = set_testfile("/testdata/categories_post.yaml")["testdata"]
        self.app.post_json('/categories', categories)
        groups = set_testfile("/testdata/item_groups_post.yaml")["testdata"]
        self.app.post_json('/item_groups', groups)
        vpe = set_testfile("/testdata/vpe_types_post.yaml")["testdata"]
        self.app.post_json('/vpe_types', vpe)
        measure = set_testfile("/testdata/unit_of_measures_post.yaml")["testdata"]
        self.app.post_json('/unit_of_measures', measure)
        items = self.testdata
        self.app.post_json('/items', items)

        resp = self.app.delete_json('/categories', {})
        assert resp.status_int == 200

        resp = self.app.delete_json('/item_groups', {})
        assert resp.status_int == 200

        resp = self.app.delete_json('/vpe_types', {})
        assert resp.status_int == 200

        resp = self.app.delete_json('/unit_of_measures', {})
        assert resp.status_int == 200

        resp = self.app.delete_json('/items', {})
        assert resp.status_int == 200


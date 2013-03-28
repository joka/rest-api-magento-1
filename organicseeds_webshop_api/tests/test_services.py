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
        self.request.validated = self.testdata
        response = categories_post(self.request)
        assert(response == {'status': 'succeeded'})

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
        existing = self.request.root.categories
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


class TestServicesVPETypesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/vpe_types_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import vpe_types_post
        self.request.validated = self.testdata
        response = vpe_types_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesUnitOfMeasuresIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/unit_of_measures_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import unit_of_measures_post
        self.request.validated = self.testdata
        response = unit_of_measures_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import items_post
        self.request.validated = self.testdata
        response = items_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesFunctional(FunctionalTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_post_invalid(self):
        jsondata = self.testdata
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

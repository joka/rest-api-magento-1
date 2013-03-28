import json

from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
    FunctionalTestCase,
)


class TestServicesCategoriesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import categories_post
        jsonstr = json.dumps(self.testdata)
        self.request.body = jsonstr
        response = categories_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemGroupsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import item_groups_post
        jsonstr = json.dumps(self.testdata)
        self.request.body = jsonstr
        response = item_groups_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesVPETypesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/vpe_types_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import vpe_types_post
        jsonstr = json.dumps(self.testdata)
        self.request.body = jsonstr
        response = vpe_types_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesUnitOfMeasuresIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/unit_of_measures_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import unit_of_measures_post
        jsonstr = json.dumps(self.testdata)
        self.request.body = jsonstr
        response = unit_of_measures_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_post(self):
        from organicseeds_webshop_api.services import items_post
        jsonstr = json.dumps(self.testdata)
        self.request.body = jsonstr
        response =  items_post(self.request)
        assert(response == {'status': 'succeeded'})


class TestServicesItemsFunctional(FunctionalTestCase):

    testdatafilepath = ("/testdata/items_post.yaml")

    def test_post(self):
        jsondata = self.testdata
        resp = self.app.post_json('/items', jsondata)
        assert resp.status_int == 200

    #def test_post_error(self):
        #jsondata = self.testdata
        #jsondata["vpe_types"][0]["id"] = "wrongid"
        #with pytest.raises(AppError):
            #self.app.post_json('/items', jsondata)


class TestServicesItemGroupsFunctional(FunctionalTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_post(self):
        jsondata = self.testdata
        resp = self.app.post_json('/item_groups', jsondata)
        assert resp.status_int == 200


class TestServicesCategoriesFunctional(FunctionalTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")

    def test_post(self):
        jsondata = self.testdata
        resp = self.app.post_json('/categories', jsondata)
        assert resp.status_int == 200


class TestServicesVPETypesFunctional(FunctionalTestCase):

    testdatafilepath = ("/testdata/vpe_types_post.yaml")

    def test_post(self):
        jsondata = self.testdata
        resp = self.app.post_json('/vpe_types', jsondata)
        assert resp.status_int == 200


class TestServicesUnitOfMeasuresFunctional(FunctionalTestCase):

    testdatafilepath = ("/testdata/unit_of_measures_post.yaml")

    def test_post(self):
        jsondata = self.testdata
        resp = self.app.post_json('/unit_of_measures', jsondata)
        assert resp.status_int == 200

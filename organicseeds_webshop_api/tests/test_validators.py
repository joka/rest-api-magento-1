from organicseeds_webshop_api.testing import (
    IntegrationTestCase,
)


class TestValidatorsBasicIntegration(IntegrationTestCase):

    def test_validate_key_unique_valid(self):
        from organicseeds_webshop_api.validators import validate_key_unique
        appstructs = {"entities": [{"id": 1}, {"id": 2}]}
        self.request.validated = appstructs
        validate_key_unique("entities", "id",  self.request)
        assert(len(self.request.errors) == 0)

    def test_validate_key_unique_invalid(self):
        from organicseeds_webshop_api.validators import validate_key_unique
        appstructs = {"entities": [{"id": 1}, {"id": 1}]}
        self.request.validated = appstructs
        validate_key_unique("entities", "id", self.request)
        assert(len(self.request.errors) == 1)

    def test_validate_key_do_not_exists_valid(self):
        from organicseeds_webshop_api.validators import\
            validate_key_does_not_exists
        appstructs = {"entities": [{"id": 1}]}
        self.request.validated = appstructs
        self.request.root.app_root["entities"] = {}
        validate_key_does_not_exists("entities", "id",  self.request)
        assert(len(self.request.errors) == 0)

    def test_validate_key_do_not_exists_invalid(self):
        from organicseeds_webshop_api.validators import\
            validate_key_does_not_exists
        appstructs = {"entities": [{"id": 1}]}
        self.request.validated = appstructs
        self.request.root.app_root["entities"] = {}
        self.request.root.app_root["entities"][1] = {"id": 1}
        validate_key_does_not_exists("entities", "id",  self.request)
        assert(len(self.request.errors) == 1)

    def test_validate_title_unique_valid(self):
        from organicseeds_webshop_api.validators import validate_title_unique
        appstructs = {"entities": [{"title": {"default": "1"}},
                                   {"title": {"default": "2", "fr":"3"}}]}
        self.request.validated = appstructs
        validate_title_unique("entities", self.request)
        assert(len(self.request.errors) == 0)

    def test_validate_title_unique_invalid(self):
        from organicseeds_webshop_api.validators import validate_title_unique
        appstructs = {"entities": [{"title": {"default": "1"}},
                                   {"title": {"default": "2", "fr":"1"}}]}
        self.request.validated = appstructs
        validate_title_unique("entities", self.request)
        assert(len(self.request.errors) == 1)

    def test_validate_title_does_not_exists_valid(self):
        from organicseeds_webshop_api.validators import\
            validate_title_does_not_exists
        appstructs = {"entities": [{"title": {"default": "1"}}]}
        self.request.validated = appstructs
        self.request.root.app_root["entities"] = {}
        self.request.root.app_root["entities"][1] = {"title": {"fr": "2"}}
        validate_title_does_not_exists("entities", self.request)
        assert(len(self.request.errors) == 0)

    def test_validate_title_does_not_exists_invalid(self):
        from organicseeds_webshop_api.validators import\
            validate_title_does_not_exists
        appstructs = {"entities": [{"title": {"default": "1"}}]}
        self.request.validated = appstructs
        self.request.root.app_root["entities"] = {}
        self.request.root.app_root["entities"][1] = {"title": {"fr": "1"}}
        validate_title_does_not_exists("entities", self.request)
        assert(len(self.request.errors) == 1)


class TestValidatorsCategoryIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/categories_post.yaml")

    def test_validator_parent_id_valid(self):
        from organicseeds_webshop_api.validators import \
            validate_category_parent_id
        self.request.validated = self.testdata
        validate_category_parent_id(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_parent_id_novalid_non_existent_id(self):
        from organicseeds_webshop_api.validators import \
            validate_category_parent_id
        self.testdata["categories"][0]['parent_id'] = u"non_existent"
        self.testdata["categories"][0]['id'] = u"1000"
        self.request.validated = self.testdata
        validate_category_parent_id(self.request)
        error_desription = 'parent_id: non_existent of category: 1000 does '\
                           'not exists and is not going to be created'
        assert(error_desription == self.request.errors[0]["description"])

    def test_validator_parent_id_nonvalid_id_eq_parent_id(self):
        from organicseeds_webshop_api.validators import \
            validate_category_parent_id
        self.testdata["categories"][0]['parent_id'] = u"1000"
        self.testdata["categories"][0]['id'] = u"1000"
        self.request.validated = self.testdata
        validate_category_parent_id(self.request)
        error_desription = 'parent_id: 1000 and id: 1000 are the same'
        assert(error_desription == self.request.errors[0]["description"])

    def test_validator_id_does_not_exists_nonvalid(self):
        from organicseeds_webshop_api.validators import \
            validate_category_id_does_not_exists
        self.testdata["categories"][0]['id'] = u"1000"
        existing = self.app_root["categories"]
        existing[u"1000"] = object()
        self.request.validated = self.testdata
        validate_category_id_does_not_exists(self.request)
        error_desription = "The following ids do already exists"\
                           " in categories: [u'1000']"
        assert(error_desription == self.request.errors[0]["description"])
        del(existing[u"1000"])

    def test_validator_id_does_not_exists_valid(self):
        from organicseeds_webshop_api.validators import \
            validate_category_id_does_not_exists
        self.testdata["categories"][0]['id'] = u"1000"
        existing = self.app_root["categories"]
        self.request.validated = self.testdata
        validate_category_id_does_not_exists(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_id_does_exists_nonvalid(self):
        from organicseeds_webshop_api.validators import \
            validate_category_id_does_exists
        existing = self.app_root["categories"]
        existing.clear()
        self.request.validated = self.testdata
        validate_category_id_does_exists(self.request)
        error_desription = "The following ids do not exists"\
                           " in categories: [1000, 1001, '1002_gemuese',"\
                           " '1002_gartenwerkzeuge', '1003_karotten']"
        assert(error_desription == self.request.errors[0]["description"])

    def test_validator_id_does_exists_valid(self):
        from organicseeds_webshop_api.validators import \
            validate_category_id_does_exists
        self.testdata["categories"][0]['id'] = 1000
        existing = self.app_root["categories"]
        existing.clear()
        existing[1000] = object()
        existing[1001] = object()
        existing[u"1002_gemuese"] = object()
        existing[u"1002_gartenwerkzeuge"] = object()
        existing[u"1003_karotten"] = object()
        self.request.validated = self.testdata
        validate_category_id_does_exists(self.request)
        assert(len(self.request.errors) == 0)


class TestValidatorsItemGroupsIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/item_groups_post.yaml")

    def test_validator_no_item_references_exist_valid(self):
        from organicseeds_webshop_api.validators import \
            validate_item_group_no_item_references_exist
        self.request.validated = self.testdata
        validate_item_group_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_no_item_references_exist_invalid(self):
        from organicseeds_webshop_api.validators import \
            validate_item_group_no_item_references_exist
        self.request.validated = self.testdata
        self.app_root["item_groups"]["sortendetail"] = {}
        self.app_root["items"]["itemid"] = {}
        self.app_root["items"]["itemid"]["parent_id"] = u"sortendetail"
        validate_item_group_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 1)


class TestValidatoresVPETypesIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/vpe_types_post.yaml")

    def test_validator_no_item_references_exist_valid(self):
        from organicseeds_webshop_api.validators import \
            validate_vpe_type_no_item_references_exist
        self.request.validated = self.testdata
        validate_vpe_type_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_no_item_references_exist_invalid(self):
        from organicseeds_webshop_api.validators import \
            validate_vpe_type_no_item_references_exist
        self.request.validated = self.testdata
        self.app_root["vpe_types"]["saatscheibe"] = {}
        self.app_root["items"]["itemid"] = {}
        self.app_root["items"]["itemid"]["vpe_type_id"] = u"saatscheibe"
        validate_vpe_type_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 1)


class TestValidatorsUnitOfMeasuresIntegration(IntegrationTestCase):

    testdatafilepath = ("/testdata/unit_of_measures_post.yaml")

    def test_validator_no_item_references_exist_valid(self):
        from organicseeds_webshop_api.validators import \
            validate_unit_of_measure_no_item_references_exist
        self.request.validated = self.testdata
        validate_unit_of_measure_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 0)

    def test_validator_no_item_references_exist_invalid(self):
        from organicseeds_webshop_api.validators import \
            validate_unit_of_measure_no_item_references_exist
        self.request.validated = self.testdata
        self.app_root["unit_of_measures"]["portion"] = {}
        self.app_root["items"]["itemid"] = {}
        self.app_root["items"]["itemid"]["unit_of_measure_id"] = u"portion"
        validate_unit_of_measure_no_item_references_exist(self.request)
        assert(len(self.request.errors) == 1)

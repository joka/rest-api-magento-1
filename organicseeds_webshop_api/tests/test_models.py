import unittest


class TestModels(unittest.TestCase):

    def test_models_data_from_appstruct(self):
        from organicseeds_webshop_api import models
        data = models.Data()
        appstruct = ({"title": {"default": "test", "fr": "testfr"},
                     "ids": [1, 2]})
        data.from_appstruct(appstruct)
        assert data["title"]["default"] == "test"

    def test_models_data_to_data(self):
        from organicseeds_webshop_api import models
        data = models.Data()
        appstruct = ({"title": {"default": "test", "fr": "testfr"}})
        data.from_appstruct(appstruct)
        assert data.to_data() == appstruct

    def test_models_data_to_data_with_lang_default(self):
        from organicseeds_webshop_api import models
        data = models.Data()
        appstruct = ({"title": {"default": "test", "fr": "testfr"},
                     "ids": [1, 2]})
        data.from_appstruct(appstruct)
        assert data.to_data("default") == {"title": "test", "ids": [1, 2]}

    def test_models_data_to_data_with_lang_not_default(self):
        from organicseeds_webshop_api import models
        data = models.Data()
        appstruct = ({"title": {"default": "test", "fr": "testfr"},
                      "ids": [1, 2]})
        data.from_appstruct(appstruct)
        assert data.to_data("fr") == {"title": "testfr", "ids": [1, 2]}

    def test_models_data_to_data_with_lang_not_default_missing(self):
        from organicseeds_webshop_api import models
        data = models.Data()
        appstruct = ({"title": {"default": "test"},
                     "ids": [1, 2]})
        data.from_appstruct(appstruct)
        assert data.to_data("fr") == {"title": "test", "ids": [1, 2]}

    def test_models_data_to_data_with_lang_default_with_attribute_lists(self):
        from organicseeds_webshop_api import models
        data = models.Data()
        appstruct = ({"title": {"default": "test"},
                     "ids": [{"id": {"default": 1, "fr": 2}}]})
        data.from_appstruct(appstruct)
        assert data.to_data("default") == {"title": "test", "ids": [{"id": 1}]}

    def test_models_data_to_data_with_lang_default_with_text_attribute_lists(self):
        from organicseeds_webshop_api import models
        data = models.Data()
        appstruct = ({"title": {"default": "test"},
                      "ids": [{"value": [{"text": {"default": "text"}}]}]})
        data.from_appstruct(appstruct)
        assert data.to_data("default") == {"title": "test",
                                           "ids": [{"value": [{"text": "text"}]}]}

    def test_models_item_group_to_data_inherited_attributes(self):
        from organicseeds_webshop_api import models
        child = models.ItemGroup()
        parent1 = models.Category()
        parent2 = models.Category()
        child.__parent__ = parent1
        parent1.__parent__ = parent2
        child["text_attributes"] = [{"id": 1, "test": 1}]
        parent2["text_attributes"] = [{"id": 1, "text": 2}]
        parent2["bool_attributes"] = [{"id": 2}]

        assert child.to_data()["text_attributes"] == [{"id": 1, "test": 1}]
        assert child.to_data()["bool_attributes"] == [{"id": 2}]

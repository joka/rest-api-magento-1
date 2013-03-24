from webtest import TestApp
import unittest
import yaml
import yaml2json

from organicseeds_webshop_api import main
from organicseeds_webshop_api import schemata


def yaml_to_json(yamlstring):
    yamldata = yaml.load(yamlstring)
    jsondata = yaml2json.convertArrays(yamldata)
    return jsondata


class TestWebshopAPI(unittest.TestCase):

    def test_categories(self):
        app = TestApp(main({}))
        jsondata = yaml_to_json(schemata.CATEGORIES_EXAMPLE_YAML)
        app.post_json('/categories', jsondata)

    def test_items(self):
        app = TestApp(main({}))
        import ipdb; ipdb.set_trace()
        jsondata = yaml_to_json(schemata.ITEMS_POST_EXAMPLE_YAML)
        app.post_json('/items', jsondata)

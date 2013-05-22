Search for entities
===================

Setup
-----
::

    >>> import yaml
    >>> import pytest
    >>> from webtest import TestApp, AppError
    >>> from organicseeds_webshop_api import main
    >>> from organicseeds_webshop_api.testing import get_file, testconfig, reset_database_with_testdata
    >>> app = TestApp(main(testconfig()))

We need some dictionaries with test data::

    >>> itemstestdata = yaml.load(get_file("/testdata/items_post.yaml"))
    >>> categoriestestdata = yaml.load(get_file("/testdata/categories_post.yaml"))
    >>> itemgroupstestdata = yaml.load(get_file("/testdata/item_groups_post.yaml"))
    >>> unitofmeasurestestdata = yaml.load(get_file("/testdata/unit_of_measures_post.yaml"))
    >>> vpestestdata = yaml.load(get_file("/testdata/vpe_types_post.yaml"))


so we can populate the webshop api without writing to the webshop (magento) database::

    >>> categoriestestdata["save_in_webshop"] = False
    >>> sink = app.post_json('/categories', categoriestestdata)
    >>> itemgroupstestdata["save_in_webshop"] = False
    >>> sink = app.post_json('/item_groups', itemgroupstestdata)
    >>> sink = app.post_json('/vpe_types', vpestestdata)
    >>> sink = app.post_json('/unit_of_measures', unitofmeasurestestdata)
    >>> itemstestdata["save_in_webshop"] = False
    >>> sink = app.post_json('/items', itemstestdata)


Search for Item or ItemGroups
-------------------------------

We want to list ItemGroups (Sortendetails) with specific attribute values in the webshop.
To do so we just have to send a get request with the desired search keywords/values (aka attribute names)::

    >>> app.get('/search', {"shop_id": "ch_hobby", "__type__": "sortendetail"})
    <200 OK application/json body='[{"bool_a...

to translated data we need to set the request parameter "lang"::

    >>> resp = app.get('/search', {"lang": "fr", "shop_id": "ch_hobby", "__type__": "sortendetail"})
    >>> resp.json_body[0]["title"]
    u'carotte'


TODO:
      get category URL
      suppport more search attributes


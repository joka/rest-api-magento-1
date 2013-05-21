Get Webshop Items, ItemGroups or Categories data
=================================================

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


Get Item data:
--------------

If we now the item id/webshopapi_id we can get the item default translation data with a simple get request::

    >>> app.get('/items/itemka32')
    <200 OK application/json body=...

to get a specific language we need to set the request parameter "lang"::

    >>> resp = app.get('/items/itemka32', {"lang": "fr"})
    >>> resp.json_body["title"]
    u'titlefr'


Get ItemGroup data:
-------------------

If we now the item_group id/webshopapi_id we can get the item_group default translation data with a simple get request::

    >>> app.get('/item_groups/33333_karottensorte')
    <200 OK application/json body=...

to get a specific language we need to set the request parameter "lang"::

    >>> resp = app.get('/item_groups/33333_karottensorte', {"lang": "fr"})
    >>> resp.json_body["title"]
    u'carotte'

to include item_group children we need to set the request parameters "with_children" and "children_shop_id"
(the "children_shop_id" is the magento store group name)::

    >>> resp = app.get('/item_groups/33333_karottensorte', {"lang": "fr", "with_children": True, "children_shop_id": "ch_hobby"})
    >>> resp.json_body["children_grouped"]
    {u'saatscheibe':...

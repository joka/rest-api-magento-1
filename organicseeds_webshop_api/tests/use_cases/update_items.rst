Update Webshop Items
====================

Setup
-----
::

    >>> import yaml
    >>> import pytest
    >>> from webtest import TestApp, AppError
    >>> from organicseeds_webshop_api import main
    >>> from organicseeds_webshop_api.testing import get_file, testconfig, reset_database_without_testdata
    >>> app = TestApp(main(testconfig()))

We need some dictionaries with test data::

    >>> itemstestdata = yaml.load(get_file("/testdata/items_post.yaml"))
    >>> categoriestestdata = yaml.load(get_file("/testdata/categories_post.yaml"))
    >>> itemgroupstestdata = yaml.load(get_file("/testdata/item_groups_post.yaml"))
    >>> unitofmeasurestestdata = yaml.load(get_file("/testdata/unit_of_measures_post.yaml"))
    >>> vpestestdata = yaml.load(get_file("/testdata/vpe_types_post.yaml"))

so we can populate the webshop api and magento database::

    >>> reset_database_without_testdata()

    >>> sink = app.post_json('/categories', categoriestestdata)
    >>> sink = app.post_json('/item_groups', itemgroupstestdata)
    >>> sink = app.post_json('/vpe_types', vpestestdata)
    >>> sink = app.post_json('/unit_of_measures', unitofmeasurestestdata)
    >>> sink = app.post_json('/items', itemstestdata)

TODO: sync magento ids: webshopapi <- magento database


Update Items:
-------------

We can update existing items, exept the parent_id, __type__, category_ids::

    >>> app.put_json('/items', {"items": [{"id": "itemka32", 'default': u'New Description' }]})
    <200 OK application/json body=...

and existing vpe_types (mind to set all fields)::

    >>> app.put_json('/vpe_types', {"vpe_types": [{"id": "saatscheibe", 'title': {"default": u'Neue Saatscheibe'}, "legend": {"default": "Legend"}}]})
    <200 OK application/json body=...


and unit_of_measures (mind to set all fields)::

    >>> app.put_json('/unit_of_measures', {"unit_of_measures": [{"id": "portion", 'title': {'default': u'New Portion'}}]})
    <200 OK application/json body=...

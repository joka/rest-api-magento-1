Update Webshop ItemGroups and Categories
==========================================

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

so we can populate the webshop api::

    >>> categoriestestdata["save_in_webshop"] = False
    >>> sink = app.post_json('/categories', categoriestestdata)
    >>> itemgroupstestdata["save_in_webshop"] = False
    >>> sink = app.post_json('/item_groups', itemgroupstestdata)
    >>> sink = app.post_json('/vpe_types', vpestestdata)
    >>> sink = app.post_json('/unit_of_measures', unitofmeasurestestdata)
    >>> itemstestdata["save_in_webshop"] = False
    >>> sink = app.post_json('/items', itemstestdata)

and the magento database::

    >>> reset_database_with_testdata()


Update Categories:
------------------

First delete Categories::

    >>> app.delete_json('/categories', {})
    <200 OK application/json...

then recreate::

    >>> app.post_json('/categories', categoriestestdata)
    <200 OK application/json...

Update ItemGroups::
--------------------

First delete ItemGroups::

    >>> app.delete_json('/item_groups', {})
    <200 OK application/json...

then recreate::

    >>> app.post_json('/item_groups', itemgroupstestdata)
    <200 OK application/json...

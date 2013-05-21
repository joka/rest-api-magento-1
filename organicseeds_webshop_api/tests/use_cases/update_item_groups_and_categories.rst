Update Webshop ItemGroups and Categories
==========================================

Setup
-----
::

    >>> import yaml
    >>> import pytest
    >>> from webtest import TestApp, AppError
    >>> from organicseeds_webshop_api import main
    >>> from organicseeds_webshop_api.testing import get_file, testconfig
    >>> app = TestApp(main(testconfig()))

We also need some dictionaries to post test data::

    >>> itemstestdata = yaml.load(get_file("/testdata/items_post.yaml"))
    >>> categoriestestdata = yaml.load(get_file("/testdata/categories_post.yaml"))
    >>> itemgroupstestdata = yaml.load(get_file("/testdata/item_groups_post.yaml"))
    >>> unitofmeasurestestdata = yaml.load(get_file("/testdata/unit_of_measures_post.yaml"))
    >>> vpestestdata = yaml.load(get_file("/testdata/vpe_types_post.yaml"))

a clean database::

    >>> sink = app.delete_json('/categories', {})
    >>> sink = app.delete_json('/item_groups', {})
    >>> sink = app.delete_json('/items', {})

and add some Items::

    >>> sink = app.post_json('/categories', categoriestestdata)
    >>> sink = app.post_json('/item_groups', itemgroupstestdata)
    >>> sink = app.post_json('/vpe_types', vpestestdata)
    >>> sink = app.post_json('/unit_of_measures', unitofmeasurestestdata)
    >>> sink = app.post_json('/items', itemstestdata)


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

TODO: Update ItemGroups, link parents/children
TODO: Update Categories, link parents/children

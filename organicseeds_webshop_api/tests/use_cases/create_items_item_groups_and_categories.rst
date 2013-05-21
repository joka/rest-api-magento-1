Create and delete Webshop Items, ItemGroups or Categories
==========================================================

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

And should start with an empty database::

    >>> sink = app.delete_json('/categories', {})
    >>> sink = app.delete_json('/item_groups', {})
    >>> sink = app.delete_json('/items', {})


Add Items, ItemGroups, and Categories
--------------------------------------

We cannot post items if referenced entities are missing::

    >>> with pytest.raises(AppError):
    ...     app.post_json('/items', itemstestdata)

So first we have to post json data to add categories::

    >>> app.post_json('/categories', categoriestestdata)
    <200 OK application/json...

item groups::

    >>> app.post_json('/item_groups', itemgroupstestdata)
    <200 OK application/json...

vpe types::

    >>> app.post_json('/vpe_types', vpestestdata)
    <200 OK application/json...

and measure units::

    >>> app.post_json('/unit_of_measures', unitofmeasurestestdata)
    <200 OK application/json...

Now we cann post items::

    >>> app.post_json('/items', itemstestdata)
    <200 OK application/json...


Deleting Items, VPE Types and Unit Of Measures
----------------------------------------------

We cannot delete vpe types or unit of measrues if they are still referenced by items::

    >>> with pytest.raises(AppError):
    ...     app.delete_json('/unit_of_measures', {})

    >>> with pytest.raises(AppError):
    ...     app.delete_json('/vpe_types', {})

So first we delete the items::

    >>> app.delete_json('/items', {})
    <200 OK application/json...

then vpe types / measures::

    >>> app.delete_json('/unit_of_measures', {})
    <200 OK application/json...

    >>> app.delete_json('/vpe_types', {})
    <200 OK application/json...


Deleting ItemGroups, Categories
--------------------------------

We can delete item groups::

    >>> app.delete_json('/item_groups', {})
    <200 OK application/json...

and categories::

    >>> app.delete_json('/categories', {})
    <200 OK application/json...


TODO: Deleting items with referenced orders possible in Magento?

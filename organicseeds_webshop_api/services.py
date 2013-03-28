# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
"""Webserservies to upload Entities to the webshop"""

import json
from pyramid.security import Everyone, Authenticated, Allow
from cornice import Service

from organicseeds_webshop_api import schemata
from organicseeds_webshop_api import models


###################
# base validators #
###################


def validate_id(data_key, request):
    entities =  request.validated[data_key]
    entity_ids = set([i["id"] for i in entities])
    app_root = request.root.app_root
    existing_folder = app_root[data_key]
    existing = set(existing_folder.keys())
    already_exists = existing.intersection(entity_ids)

    error = 'The following ids do already exists in %s: %s'
    if already_exists:
        request.errors.add('body', 'id',
                            error  % (data_key, [x for x in already_exists].__str__()))


#######################
# /categories service #
#######################


categories = Service(name='categories',
                     path='/categories',
                     description="Service to upload webshop categories")


def validate_category_id(request):
    validate_id("categories", request)


def validate_category_parent_id(request):
    categories =  request.validated["categories"]
    new_ids= [i["id"] for i in categories]
    app_root = request.root.app_root
    existing_ids = [x for x in app_root["categories"].keys()]
    for i in categories:
        cid = i["id"]
        parent_id = i["parent_id"]
        if cid == parent_id:
            # Note: circle structures are not detected
            error = 'parent_id: %s and id: %s are the same' % (parent_id, cid)
            request.errors.add('body', 'parent_id', error)
        if parent_id == None:
            continue
        if parent_id not in new_ids + existing_ids:
            error = "parent_id: %s of category: %s does not exists"\
                    " and is not going to be created" % (parent_id, cid)
            request.errors.add('body', 'parent_id', error)


@categories.post(schema=schemata.CategoriesList, accept="text/json",
                 validators=(validate_category_parent_id,
                             validate_category_id))
def categories_post(request):
    """method : POST

       content_type: text/json

       path : categories

       body : Sequence of Category

       return codes: 200, 400
    """

    models.transform_to_python_and_store(request.validated,
                                        models.Category, "categories", request)
    return {"status": "succeeded"}


########################
# /item_groups service #
########################


item_groups = Service(name='item_groups',
                      path='/item_groups',
                      description="Service to upload item groups (like Sortendetails)")


def validate_item_group_id(request):
    validate_id("item_groups", request)


def validate_item_group_parent_id(request):
    item_groups =  request.validated["item_groups"]
    item_group_parent_ids = set([i["parent_id"] for i in item_groups])
    app_root = request.root.app_root
    existing = set(app_root["categories"].keys())
    non_existing = item_group_parent_ids.difference(existing)

    error = 'The following parent_ids do no exists in categories: %s'
    if non_existing:
        request.errors.add('body', 'parent_id',
                            error  % ([x for x in non_existing].__str__()))


@item_groups.post(schema=schemata.ItemGroupsList, accept="text/json",
                  validators=(validate_item_group_id,
                              validate_item_group_parent_id))
def item_groups_post(request):
    """method : POST

       content_type: text/json

       path : item_groups

       body :

       * item_groups : Sequence of ItemGroup

       return codes: 200, 400
    """

    models.transform_to_python_and_store(request.validated,
                                         models.ItemGroup, "item_groups", request)
    return {"status": "succeeded"}


#############################
# /unit_of_measures service #
#############################


unit_of_measures = Service(name='unit_of_measures',
                path='/unit_of_measures',
                description="Service to upload unit_of_measures")


def validate_unit_of_measure_id(request):
    validate_id("unit_of_measures", request)


@unit_of_measures.post(schema=schemata.UnitOfMeasuresList, accept="text/json",
                       validators=(validate_unit_of_measure_id,))
def unit_of_measures_post(request):
    """method : POST

       content_type: text/json

       path : unit_of_measures

       body : Sequence of UnitOfMeasure

       return codes: 200, 400
    """

    models.transform_to_python_and_store(request.validated,
                                         models.EntityData, "unit_of_measures", request)
    return {"status": "succeeded"}


######################
# /vpe_types service #
######################


vpe_types = Service(name='vpe_types',
                path='/vpe_types',
                description="Service to upload vpe_types")


def validate_vpe_type_id(request):
    validate_id("vpe_types", request)


@vpe_types.post(schema=schemata.VPETypesList, accept="text/json",
                validators=(validate_vpe_type_id,))
def vpe_types_post(request):
    """method : POST

       content_type: text/json

       path : vpe_types

       body : Sequence of VPEType

       return codes: 200, 400
    """

    models.transform_to_python_and_store(request.validated,
                                         models.EntityData, "vpe_types", request)
    return {"status": "succeeded"}


##################
# /items service #
##################


items = Service(name='items',
                path='/items',
                description="Service to upload items")

#TODO validate item quality_id


def validate_item_id(request):
    validate_id("items", request)


def validate_item_parent_id(request):
    items =  request.validated["items"]
    item_parent_ids = set([i["parent_id"] for i in items])
    app_root = request.root.app_root
    categories = set(app_root["categories"].keys())
    item_groups = set(app_root["item_groups"].keys())
    existing = set.union(categories, item_groups)
    non_existing = item_parent_ids.difference(existing)

    error = 'The following parent_ids do no exists in item_groups or categories: %s'
    if non_existing:
        request.errors.add('body', 'parent_id',
                            error  % ([x for x in non_existing].__str__()))


def validate_item_vpe_type_id(request):
    items =  request.validated["items"]
    item_vpe_type_ids = set([i["vpe_type_id"] for i in items])
    app_root = request.root.app_root
    existing = set(app_root["vpe_types"].keys())
    non_existing = item_vpe_type_ids.difference(existing)

    error = 'The following vpe_type_ids do no exists in vpe_types: %s'
    if non_existing:
        request.errors.add('body', 'vpe_type_id',
                            error  % ([x for x in non_existing].__str__()))


def validate_item_unit_of_measure_id(request):
    items =  request.validated["items"]
    item_unit_of_measure_ids = set([i["unit_of_measure_id"] for i in items])
    app_root = request.root.app_root
    existing = set(app_root["unit_of_measures"].keys())
    non_existing = item_unit_of_measure_ids.difference(existing)

    error = 'The following unit_of_measure_ids do no exists in unit_of_measures: %s'
    if non_existing:
        request.errors.add('body', 'unit_of_measur_id',
                            error  % ([x for x in non_existing].__str__()))


@items.post(schema=schemata.ItemsList, accept="text/json",
            validators=(validate_item_id,
                        validate_item_parent_id,
                        validate_item_vpe_type_id,
                        validate_item_unit_of_measure_id))
def items_post(request):
    """method : POST

       content_type: text/json

       path : items

       body : Sequence of Item

       return codes: 200, 400
    """

    models.transform_to_python_and_store(request.validated,
                                         models.Item, "items", request)
    return {"status": "succeeded"}


@items.delete(accept="text/json")
def items_delete(request):
    """method : DELETE

       content_type: text/json

       path : items

       body :

       return codes: 200, 400
    """

    models.delete(request.validated, models.Item, "items", request)
    # TODO raise errors
    return {"status": "succeeded"}


def find_element(path, context):
    subpaths = path.split("/")
    ob = context
    for subpath in subpaths:
        ob = ob[subpath]
    return ob

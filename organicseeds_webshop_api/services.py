# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
"""Webserservies to create webshop entities"""

import json
from pyramid.security import Everyone, Authenticated, Allow
from cornice import Service

from organicseeds_webshop_api import schemata
from organicseeds_webshop_api import models


###################
# base validators #
###################


def validate_id_does_not_exists(data_key, request):
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


def validate_id_does_exists(data_key, request):
    entities =  request.validated[data_key]
    entity_ids = set([i["id"] for i in entities])
    app_root = request.root.app_root
    existing_folder = app_root[data_key]
    existing = set(existing_folder.keys())
    not_existing = entity_ids.difference(existing)

    error = 'The following ids do not exists in %s: %s'
    if not_existing:
        request.errors.add('body', 'id',
                            error  % (data_key, [x for x in not_existing].__str__()))


def validate_no_reference_ids_exist(data_key, data_key_refs,
                                    attr_ref_id, request):
    app_root = request.root.app_root
    entity_ids = app_root[data_key].keys()
    entity_refs = app_root[data_key_refs].values()
    entity_refs_ids = [x[attr_ref_id] for x in entity_refs]

    existing_references = set(entity_refs_ids).intersection(set(entity_ids))

    error = 'The following %s are still referenced in %s: %s'
    if existing_references:
        request.errors.add('body', data_key_refs,
                            error  % (data_key, data_key_refs, [x for x in existing_references].__str__()))


#######################
# /categories service #
#######################


categories = Service(name='categories',
                     path='/categories',
                     description="Service to upload webshop categories")


def validate_category_id_does_not_exists(request):
    validate_id_does_not_exists("categories", request)


def validate_category_id_does_exists(request):
    validate_id_does_exists("categories", request)


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


def validate_no_item_group_references_exist(request):
    validate_no_reference_ids_exist("categories", "item_groups", "parent_id", request)


@categories.post(schema=schemata.CategoriesList, accept="text/json",
                 validators=(validate_category_parent_id,
                             validate_category_id_does_not_exists))
def categories_post(request):
    """Create new category entities

       method : POST

       content_type: text/json

       path : categories

       body :

       * Sequence of Category

       return codes: 200, 400, 500
    """

    models.transform_to_python_and_store(request.validated,
                                        models.Category, "categories", request)
    #TODO update parent links
    #TODO update category children,
    return {"status": "succeeded"}


@categories.delete(accept="text/json",
                   validators=(validate_no_item_group_references_exist))
def categories_delete(request):
    """Delete category entities.
       You should delete item_group children first.

       method : DELETE

       content_type: text/json

       path : categories

       body :

       return codes: 200, 400, 500
    """

    models.delete(request.validated, models.Category, "categories", request)
    # TODO raise errors
    return {"status": "succeeded"}


########################
# /item_groups service #
########################


item_groups = Service(name='item_groups',
                      path='/item_groups',
                      description="Service to upload item groups (like Sortendetails)")


def validate_item_group_id_does_not_exists(request):
    validate_id_does_not_exists("item_groups", request)


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


def validate_item_group_no_item_references_exist(request):
    validate_no_reference_ids_exist("item_groups", "items", "parent_id", request)


@item_groups.post(schema=schemata.ItemGroupsList, accept="text/json",
                  validators=(validate_item_group_id_does_not_exists,
                              validate_item_group_parent_id))
def item_groups_post(request):
    """Create new item group entities

       method : POST

       content_type: text/json

       path : item_groups

       body :

       * item_groups : Sequence of ItemGroup

       return codes: 200, 400, 500
    """

    models.transform_to_python_and_store(request.validated,
                                         models.ItemGroup, "item_groups", request)
    #TODO update parent links
    #TODO update category children,
    return {"status": "succeeded"}


@item_groups.delete(accept="text/json")
def item_groups_delete(request):
    """Delete item group entities

       method : DELETE

       content_type: text/json

       path : item_groups

       body :

       return codes: 200, 400, 500
    """

    models.delete(request.validated, models.Item, "item_groups", request)
    return {"status": "succeeded"}


#############################
# /unit_of_measures service #
#############################


unit_of_measures = Service(name='unit_of_measures',
                path='/unit_of_measures',
                description="Service to upload unit_of_measures")


def validate_unit_of_measure_id_does_not_exists(request):
    validate_id_does_not_exists("unit_of_measures", request)


def validate_unit_of_measure_no_item_references_exist(request):
    validate_no_reference_ids_exist("unit_of_measures", "items", "unit_of_measure_id", request)


@unit_of_measures.post(schema=schemata.UnitOfMeasuresList, accept="text/json",
                       validators=(validate_unit_of_measure_id_does_not_exists,))
def unit_of_measures_post(request):
    """Create new unit of measure data (for items)

       method : POST

       content_type: text/json

       path : unit_of_measures

       body :

       * Sequence of UnitOfMeasure

       return codes: 200, 400, 500
    """

    models.transform_to_python_and_store(request.validated,
                                         models.EntityData, "unit_of_measures", request)
    return {"status": "succeeded"}


@unit_of_measures.delete(accept="text/json",
                  validators=validate_unit_of_measure_no_item_references_exist)
def unit_of_measures_delete(request):
    """Delete unit of measure data

       method : DELETE

       content_type: text/json

       path : unit_of_measures

       body :

       return codes: 200, 400, 500
    """

    models.delete(request.validated, models.Item, "unit_of_measures", request)
    # TODO raise errors
    return {"status": "succeeded"}


######################
# /vpe_types service #
######################


vpe_types = Service(name='vpe_types',
                path='/vpe_types',
                description="Service to upload vpe_types")


def validate_vpe_type_id_does_not_exists(request):
    validate_id_does_not_exists("vpe_types", request)


def validate_vpe_type_no_item_references_exist(request):
    validate_no_reference_ids_exist("vpe_types", "items", "vpe_type_id", request)


@vpe_types.post(schema=schemata.VPETypesList, accept="text/json",
                validators=(validate_vpe_type_id_does_not_exists,))
def vpe_types_post(request):
    """Create new vpe type data (for items).
       You should delete referencing items first.

       method : POST

       content_type: text/json

       path : vpe_types

       body :

       * Sequence of VPEType

       return codes: 200, 400, 500
    """

    models.transform_to_python_and_store(request.validated,
                                         models.EntityData, "vpe_types", request)
    return {"status": "succeeded"}


@vpe_types.delete(accept="text/json",
                  validators=validate_vpe_type_no_item_references_exist)
def vpe_types_delete(request):
    """Delete vpe type data (for items).
       You should delete referencing items first.

       method : DELETE

       content_type: text/json

       path : vpe_types

       body :

       return codes: 200, 400, 500
    """

    models.delete(request.validated, models.Item, "vpe_types", request)
    # TODO raise errors
    return {"status": "succeeded"}


##################
# /items service #
##################


items = Service(name='items',
                path='/items',
                description="Service to upload items")

#TODO validate item quality_id


def validate_item_id_does_not_exists(request):
    validate_id_does_not_exists("items", request)


def validate_item_id_does_exists(request):
    validate_id_does_exists("items", request)


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
            validators=(validate_item_id_does_not_exists,
                        validate_item_parent_id,
                        validate_item_vpe_type_id,
                        validate_item_unit_of_measure_id))
def items_post(request):
    """Create new item entities

       method : POST

       content_type: text/json

       path : items

       body :

       * Sequence of Item

       return codes: 200, 400, 500
    """

    models.transform_to_python_and_store(request.validated,
                                         models.Item, "items", request)
    #TODO update parent links
    #TODO update item_group/category children
    return {"status": "succeeded"}


@items.put(schema=schemata.ItemsUpdateList, accept="text/json",
            validators=(validate_item_id_does_exists,
                        validate_item_parent_id,
                        validate_item_vpe_type_id,
                        validate_item_unit_of_measure_id))
def items_put(request):
    """Update existing item entities

       method : PUT

       content_type: text/json

       path : items

       body :

       * Sequence of ItemUpdate

       return codes: 200, 400, 500
    """

    #models.transform_to_python_and_update(request.validated,
                                         #models.Item, "items", request)
    #TODO update parent links
    #TODO update item_group/category children
    return {"status": "succeeded"}


@items.delete(accept="text/json")
def items_delete(request):
    """Delete item entities

       method : DELETE

       content_type: text/json

       path : items

       body :

       return codes: 200, 400, 500
    """

    models.delete(request.validated, models.Item, "items", request)
    #TODO update item_group/category children
    return {"status": "succeeded"}


#def find_element(path, context):
    #subpaths = path.split("/")
    #ob = context
    #for subpath in subpaths:
        #ob = ob[subpath]
    #return ob

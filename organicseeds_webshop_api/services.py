# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
"""Webserservies to create webshop entities"""

#from pyramid.security import Everyone, Authenticated, Allow
from cornice import Service

from organicseeds_webshop_api import schemata
from organicseeds_webshop_api import models
from organicseeds_webshop_api import validators
from organicseeds_webshop_api import utils


#######################
# /categories service #
#######################


categories = Service(name='categories',
                     path='/categories',
                     description="Service to upload webshop categories")


@categories.post(schema=schemata.CategoriesList, accept="text/json",
                 validators=(validators.validate_category_parent_id,
                             validators.validate_category_id_does_not_exists))
def categories_post(request):
    """Create new category entities

       method : POST

       content_type: text/json

       path : categories

       body :

       * Sequence of Category

       return codes: 200, 400, 500
    """

    utils.transform_to_python_and_store(request.validated, models.Category,
                                         "categories", request)
    #TODO update parent links
    #TODO update category children,
    return {"status": "succeeded"}


@categories.delete(
    accept="text/json",
    validators=(validators.validate_no_item_group_references_exist))
def categories_delete(request):
    """Delete category entities.
       You should delete item_group children first.

       method : DELETE

       content_type: text/json

       path : categories

       body :

       return codes: 200, 400, 500
    """

    utils.delete(request.validated, models.Category, "categories", request)
    # TODO raise errors
    return {"status": "succeeded"}


#########################
# /item_groups service  #
#########################


item_groups = Service(name='item_groups',
                      path='/item_groups',
                      description="Service to upload item groups"
                                  " (like Sortendetails)")


@item_groups.post(
    schema=schemata.ItemGroupsList, accept="text/json",
    validators=(validators.validate_item_group_id_does_not_exists,
                validators.validate_item_group_parent_id))
def item_groups_post(request):
    """Create new item group entities

       method : POST

       content_type: text/json

       path : item_groups

       body :

       * item_groups : Sequence of ItemGroup

       return codes: 200, 400, 500
    """

    utils.transform_to_python_and_store(request.validated, models.ItemGroup,
                                         "item_groups", request)
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

    utils.delete(request.validated, models.Item, "item_groups", request)
    return {"status": "succeeded"}


#############################
# /unit_of_measures service #
#############################


unit_of_measures = Service(name='unit_of_measures',
                           path='/unit_of_measures',
                           description="Service to upload unit_of_measures")


@unit_of_measures.post(
    schema=schemata.UnitOfMeasuresList, accept="text/json",
    validators=(validators.validate_unit_of_measure_id_does_not_exists))
def unit_of_measures_post(request):
    """Create new unit of measure data (for items)

       method : POST

       content_type: text/json

       path : unit_of_measures

       body :

       * Sequence of UnitOfMeasure

       return codes: 200, 400, 500
    """

    utils.transform_to_python_and_store(request.validated,
                                         models.EntityData,
                                         "unit_of_measures", request)
    return {"status": "succeeded"}


@unit_of_measures.delete(
    accept="text/json",
    validators=validators.validate_unit_of_measure_no_item_references_exist)
def unit_of_measures_delete(request):
    """Delete unit of measure data

       method : DELETE

       content_type: text/json

       path : unit_of_measures

       body :

       return codes: 200, 400, 500
    """

    utils.delete(request.validated, models.Item, "unit_of_measures", request)
    # TODO raise errors
    return {"status": "succeeded"}


######################
# /vpe_types service #
######################


vpe_types = Service(name='vpe_types',
                    path='/vpe_types',
                    description="Service to upload vpe_types")


@vpe_types.post(schema=schemata.VPETypesList, accept="text/json",
                validators=(validators.validate_vpe_type_id_does_not_exists,))
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

    utils.transform_to_python_and_store(request.validated,
                                         models.EntityData, "vpe_types",
                                         request)
    return {"status": "succeeded"}


@vpe_types.delete(
    accept="text/json",
    validators=validators.validate_vpe_type_no_item_references_exist)
def vpe_types_delete(request):
    """Delete vpe type data (for items).
       You should delete referencing items first.

       method : DELETE

       content_type: text/json

       path : vpe_types

       body :

       return codes: 200, 400, 500
    """

    utils.delete(request.validated, models.Item, "vpe_types", request)
    # TODO raise errors
    return {"status": "succeeded"}


##################
# /items service #
##################


items = Service(name='items',
                path='/items',
                description="Service to upload items")
#TODO validate item quality_id


@items.post(schema=schemata.ItemsList, accept="text/json",
            validators=(validators.validate_item_id_does_not_exists,
                        validators.validate_item_parent_id,
                        validators.validate_item_vpe_type_id,
                        validators.validate_item_unit_of_measure_id))
def items_post(request):
    """Create new item entities

       method : POST

       content_type: text/json

       path : items

       body :

       * Sequence of Item

       return codes: 200, 400, 500
    """

    utils.transform_to_python_and_store(request.validated,
                                         models.Item, "items", request)
    #TODO update parent links
    #TODO update item_group/category children
    return {"status": "succeeded"}


@items.put(schema=schemata.ItemsUpdateList, accept="text/json",
           validators=(validators.validate_item_id_does_exists))
def items_put(request):
    """Update existing item entities

       method : PUT

       content_type: text/json

       path : items

       body :

       * Sequence of ItemUpdate

       return codes: 200, 400, 500
    """
    # filter non existing fields in data
    for item in request.validated["items"]:
        for i, v in item.items():
            if v is None:
                del(item[i])
    # store data
    utils.transform_to_python_and_store(request.validated, models.Item,
                                         "items", request)
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

    utils.delete(request.validated, models.Item, "items", request)
    #TODO update item_group/category children
    return {"status": "succeeded"}


#def find_element(path, context):
    #subpaths = path.split("/")
    #ob = context
    #for subpath in subpaths:
        #ob = ob[subpath]
    #return ob

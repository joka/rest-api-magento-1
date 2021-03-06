# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
"""Webserservies to create webshop entities"""

#from pyramid.security import Everyone, Authenticated, Allow
from cornice import Service

from organicseeds_webshop_api import exceptions
from organicseeds_webshop_api import schemata
from organicseeds_webshop_api import models
from organicseeds_webshop_api import validators
from organicseeds_webshop_api import utils
from organicseeds_webshop_api import magentoapi


#######################
# /categories service #
#######################


categories = Service(name='categories',
                     path='/categories',
                     description="Service to upload webshop categories")


@categories.post(schema=schemata.CategoriesList, accept="text/json",
                 validators=(validators.validate_category_parent_id,
                             validators.validate_category_id_unique,
                             validators.validate_category_id_does_not_exists,
                             ))
def categories_post(request):
    """Create new category entities

       request body :

           * categories: Sequence of Category
    """

    save_in_webshop = request.validated.get("save_in_webshop", True)
    appstructs = request.validated["categories"]
    categories = utils.store(appstructs, models.Category, "categories",
                             request)
    if save_in_webshop:
        with magentoapi.Categories(request) as proxy:
            try:
                # create categories in webshop
                webshop_ids = proxy.create(appstructs)
                utils.set_webshop_ids(categories, webshop_ids)
                # activate categories in webshop shops
                proxy.update_shops(webshop_ids, appstructs)
                # link category children in webshop
                item_webshop_ids, items = utils.get_entities_item_children(
                    categories, request)
                proxy.link_category_parents(item_webshop_ids, items)
            except exceptions._502 as e:
                proxy.delete([x for x in e.success if isinstance(x, int)])
                raise
        magentoapi.indexing_reindex(request)
    return {"status": "succeeded"}


@categories.delete(accept="text/json",)
def categories_delete(request):
    """Delete category entities.
       You should delete item_group children first.
    """

    utils.delete_all("categories", request)
    with magentoapi.Categories(request) as proxy:
        proxy.delete_all()
    magentoapi.indexing_reindex(request)
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
    validators=(validators.validate_item_group_id_unique,
                validators.validate_item_group_id_does_not_exists,
                validators.validate_item_group_title_unique,
                validators.validate_item_group_title_does_not_exists,
                validators.validate_item_group_parent_id
                ))
def item_groups_post(request):
    """Create new item group entities

       request body :

       * item_groups : Sequence of ItemGroup
    """

    save_in_webshop = request.validated.get("save_in_webshop", True)
    appstructs = request.validated["item_groups"]
    item_groups = utils.store(appstructs, models.ItemGroup,
                              "item_groups", request)
    if save_in_webshop:
        with magentoapi.ItemGroups(request) as proxy:
            try:
                # create item_groups in webshop
                webshop_ids = proxy.create(appstructs)
                utils.set_webshop_ids(item_groups, webshop_ids)
                # activate categories in webshop shops
                proxy.update_shops(webshop_ids, appstructs)
                # link item_group parents in webshop
                proxy.link_item_parents(webshop_ids, appstructs)
                # link item_group children in webshop
                item_webshop_ids, items = utils.get_entities_item_children(
                    item_groups, request)
                proxy.link_item_parents(item_webshop_ids, items)
            except exceptions._502 as e:
                proxy.delete([x for x in e.success if isinstance(x, int)])
                raise
        magentoapi.indexing_reindex(request)
    return {"status": "succeeded"}


@item_groups.delete(accept="text/json")
def item_groups_delete(request):
    """Delete item group entities
    """

    utils.delete_all("item_groups", request)
    with magentoapi.ItemGroups(request) as proxy:
        proxy.delete_all()
    magentoapi.indexing_reindex(request)
    return {"status": "succeeded"}


#############################
# /unit_of_measures service #
#############################


unit_of_measures = Service(name='unit_of_measures',
                           path='/unit_of_measures',
                           description="Service to upload unit_of_measures")


@unit_of_measures.post(
    schema=schemata.UnitOfMeasuresList, accept="text/json",
    validators=(validators.validate_unit_of_measure_id_unique,
                validators.validate_unit_of_measure_id_does_not_exists))
def unit_of_measures_post(request):
    """Create new unit of measure data (for items)

       reqeust body :

       * Sequence of UnitOfMeasure
    """

    utils.store(request.validated["unit_of_measures"], models.EntityData,
                "unit_of_measures", request)
    return {"status": "succeeded"}


@unit_of_measures.put(
    schema=schemata.UnitOfMeasuresList, accept="text/json",
    validators=(validators.validate_unit_of_measure_id_does_exists))
def unit_of_measures_put(request):
    """Update unit of measure data (for items)

       reqeust body :

       * Sequence of UnitOfMeasure
    """

    utils.store(request.validated["unit_of_measures"], models.EntityData,
                "unit_of_measures", request)
    return {"status": "succeeded"}


@unit_of_measures.delete(
    accept="text/json",
    validators=validators.validate_unit_of_measure_no_item_references_exist)
def unit_of_measures_delete(request):
    """Delete unit of measure data
    """

    utils.delete_all("unit_of_measures", request)
    return {"status": "succeeded"}


######################
# /vpe_types service #
######################


vpe_types = Service(name='vpe_types',
                    path='/vpe_types',
                    description="Service to upload vpe_types")


@vpe_types.post(schema=schemata.VPETypesList, accept="text/json",
                validators=(validators.validate_vpe_type_id_unique,
                            validators.validate_vpe_type_id_does_not_exists))
def vpe_types_post(request):
    """Create new vpe type data (for items).
       You should delete referencing items first.

       request body :

       * vpe_types: Sequence of VPEType
    """

    utils.store(request.validated["vpe_types"], models.EntityData,
                "vpe_types", request)
    return {"status": "succeeded"}


@vpe_types.put(schema=schemata.VPETypesList, accept="text/json",
               validators=(validators.validate_vpe_type_id_does_exists))
def vpe_types_put(request):
    """Update vpe type data (for items).

       request body :

       * vpe_types: Sequence of VPEType
    """

    utils.store(request.validated["vpe_types"], models.EntityData,
                "vpe_types", request)
    return {"status": "succeeded"}


@vpe_types.delete(
    accept="text/json",
    validators=validators.validate_vpe_type_no_item_references_exist)
def vpe_types_delete(request):
    """Delete vpe type data (for items).
       You should delete referencing items first.
    """

    utils.delete_all("vpe_types", request)
    return {"status": "succeeded"}


##################
# /items service #
##################


items = Service(name='items',
                path='/items',
                description="Service to upload items")


@items.post(schema=schemata.ItemsList, accept="text/json",
            validators=(validators.validate_items_id_unique,
                        validators.validate_items_id_does_not_exists,
                        validators.validate_items_sku_unique,
                        validators.validate_items_sku_does_not_exists,
                        validators.validate_item_parent_id,
                        validators.validate_item_vpe_type_id,
                        validators.validate_item_unit_of_measure_id,
                        ))
def items_post(request):
    """Create new item entities

       body :

       * Sequence of Item
    """
    save_in_webshop = request.validated.get("save_in_webshop", True)
    appstructs = request.validated["items"]
    items = utils.store(appstructs, models.Item, "items", request)
    if save_in_webshop:
        magentoapi.indexing_enable_manual(request)
        with magentoapi.Items(request) as proxy:
            try:
                webshop_ids = proxy.create(appstructs)
                utils.set_webshop_ids(items, webshop_ids)
                proxy.update_shops(webshop_ids, appstructs)
                proxy.link_item_parents(webshop_ids, appstructs)
            except exceptions._502 as e:
                proxy.delete([x for x in e.success if isinstance(x, int)])
                raise
        magentoapi.indexing_reindex(request)
    return {"status": "succeeded"}


@items.put(schema=schemata.ItemsUpdateList, accept="text/json",
           validators=(validators.validate_item_id_does_exists))
def items_put(request):
    """Update existing item entities

       request body :

       * items: Sequence of ItemUpdate
    """
    save_in_webshop = request.validated.get("save_in_webshop", True)
    appstructs = utils.remove_none_values(request.validated["items"])
    utils.store(appstructs, models.Item, "items", request)
    items = request.root.app_root["items"]
    if save_in_webshop:
        magentoapi.indexing_enable_manual(request)
        with magentoapi.Items(request) as proxy:
            webshop_ids = []
            for a in appstructs:
                webshop_id = items[a["id"]].webshop_id
                webshop_ids.append(webshop_id)
            proxy.update(appstructs)
            proxy.update_shops(webshop_ids, appstructs)
            magentoapi.indexing_reindex(request)
    return {"status": "succeeded"}


@items.delete(accept="text/json")
def items_delete(request):
    """Delete item entities
    """

    utils.delete_all("items", request)
    magentoapi.indexing_enable_manual(request)
    with magentoapi.Items(request) as proxy:
        proxy.delete_all()
    magentoapi.indexing_reindex(request)
    return {"status": "succeeded"}


#########################
# /orders service       #
#########################


orders = Service(name='orders',
                 path='/orders',
                 description="Service to get order data")


@orders.get(schema=schemata.OrdersGet)
def orders_get(request):
    """Get orders data

       querystring: OrdersGet schema

       response body:

           * orders: sequence of Orders
    """
    status = request.validated.get("status")
    orders = []
    with magentoapi.SalesOrders(request) as proxy:
        orders = proxy.list(status=status)
    return {"orders": orders}


@orders.put(schema=schemata.OrderUpdatesList)
def orders_put(request):
    """Add comments or change status of orders

       request body :

        * orders: * Sequence of OrderUpdate
    """
    appstructs = request.validated["orders"]
    with magentoapi.SalesOrders(request) as proxy:
        proxy.order_add_comment(appstructs)
    return {"status": "succeeded"}


#########################
# /invoices service     #
#########################


invoices = Service(name='invoices',
                   path='/invoices',
                   description="Service to create and catpure invoices")


@invoices.put(schema=schemata.InvoicesList)
def invoices_put(request):
    """Add and capture invoices

       request body:

           * invoices: Sequence of Invoices

       response body:

           *  invoice_results: Sequence of InvoiceResults
              (payment capture information)
    """
    appstructs = request.validated["invoices"]
    results = []
    with magentoapi.SalesInvoices(request) as proxy:
        # create invoices
        invoice_ids = proxy.create(appstructs)
        for i, appstruct in zip(invoice_ids, appstructs):
            # create result data
            result = schemata.InvoiceResult().serialize()
            result["invoice_increment_id"] = i
            order_id = appstruct["order_increment_id"]
            result["order_increment_id"] = order_id
            # change order state to processing
            appstruct_comment = {"order_increment_id": order_id,
                                 "status": "processing"}
            proxy.order_add_comment([appstruct_comment])
            # capture invoice if possible
            try:
                can_capture = appstruct["capture_online_payment"]\
                    and proxy.order_can_capture(order_id)
                if can_capture:
                    captured = proxy.capture(i)
                    appstruct["capture_status"] = "captured" if captured\
                        else "no-capture"
            except exceptions._502 as e:
                error = e.errors[0]
                appstruct["capture_status"] = "error"
                appstruct["capture_error"] = error[0] + ": " + error[1]
            results.append(result)
    return {"invoice_results": results}


#######################
# /items/<id> service #
#######################


item = Service(name='item',
               path='/items/{id}',
               description="Service to get item data")


#TODO use validators here
@item.get(schema=schemata.ItemGet)
def item_get(request):
    """Get item data

       querystring: ItemGet schema
    """

    item_id = request.validated["id"]
    lang = request.validated["lang"]
    try:
        item = request.root.app_root["items"][item_id]
        data = item.to_data(lang)
    except KeyError:
        error = "%s does not exists"
        raise exceptions._400(msgs=[("querystring", "id", error % (item_id))])
    return data


#############################
# /item_groups/<id> service #
#############################


item_group = Service(name='item_group',
                     path='/item_groups/{id}',
                     description="Service to get item_group data")


#TODO use validators here
@item_group.get(schema=schemata.ItemGroupGet)
def item_group_get(request):
    """Get item_group data

       querystring: ItemGroupGet schema
    """

    item_group_id = request.validated["id"]
    lang = request.validated["lang"]
    with_children = request.validated["with_children"]
    children_shop_id = request.validated["children_shop_id"]
    try:
        item_group = request.root.app_root["item_groups"][item_group_id]
        data = item_group.to_data(lang, with_children, children_shop_id)
    except KeyError:
        error = "%s does not exists"
        raise exceptions._400(msgs=[("querystring", "id",
                                     error % (item_group_id))])
    return data


#################################
# /search                       #
#################################

search_ = Service(name='search',
                  path='/search',
                  description="Service to search for entities")


@search_.get(validators=validators.validate_search_parameters)
def search_get(request):
    """Search for itemgroups

       querystring:

       * lang: language # default = "default"

       * operator: "AND" | "OR", default "AND"

       * multiple search key/value pairs,
         allowed search keys are: "shop_id" | "parent_id" | ...

    """
    lang = request.validated.pop("lang")
    operator = request.validated.pop("operator")
    search_parameters = request.validated
    result = []
    search_result = utils.search(request, operator=operator,
                                 **search_parameters)
    for entity in search_result:
        entity_data = entity.to_data(lang=lang)
        result.append(entity_data)
    return result

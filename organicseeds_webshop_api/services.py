import json
import transaction
from pyramid.security import Everyone, Authenticated, Allow
from cornice import Service

from organicseeds_webshop_api import schemata
from organicseeds_webshop_api import models


categories = Service(name='categories',
                     path='/categories',
                     description="Service to upload webshop categories")

item_groups = Service(name='item_groups',
                      path='/item_groups',
                      description="Service to upload item groups (like Sortendetails)")

unit_of_measures = Service(name='unit_of_measures',
                path='/unit_of_measures',
                description="Service to upload unit_of_measures")

vpe_types = Service(name='vpe_types',
                path='/vpe_types',
                description="Service to upload vpe_types")

items = Service(name='items',
                path='/items',
                description="Service to upload items")


def find_element(path, context):
    subpaths = path.split("/")
    ob = context
    for subpath in subpaths:
        ob = ob[subpath]
    return ob


@categories.post(schema=schemata.CategoriesList, accept="text/json")
def categories_post(request):
    """method : POST

       content_type: text/json

       path : categories

       body : Sequence of Category

       return codes: 200, 400
    """
    data = json.loads(request.body)
    models.transform_to_python_and_store(data["categories"],
                                        "Category", "categories", request)
    return {"status": "succeeded"}


@item_groups.post(schema=schemata.ItemGroupsList, accept="text/json")
def item_groups_post(request):
    """method : POST

       content_type: text/json

       path : item_groups

       body :

       * item_groups : Sequence of ItemGroup

       return codes: 200, 400
    """
    data = json.loads(request.body)
    models.transform_to_python_and_store(data["item_groups"],
                                         "ItemGroup", "item_groups", request)
    return {"status": "succeeded"}


@unit_of_measures.post(schema=schemata.UnitOfMeasuresList, accept="text/json")
def unit_of_measures_post(request):
    """method : POST

       content_type: text/json

       path : unit_of_measures

       body : Sequence of UnitOfMeasure

       return codes: 200, 400
    """

    data = json.loads(request.body)
    models.transform_to_python_and_store(data["unit_of_measures"],
                                         "UnitOfMeasure", "unit_of_measures", request)
    return {"status": "succeeded"}


@vpe_types.post(schema=schemata.VPETypesList, accept="text/json")
def vpe_types_post(request):
    """method : POST

       content_type: text/json

       path : vpe_types

       body : Sequence of VPEType

       return codes: 200, 400
    """

    data = json.loads(request.body)
    models.transform_to_python_and_store(data["vpe_types"],
                                         "VPEType", "vpe_types", request)
    return {"status": "succeeded"}


@items.post(schema=schemata.ItemsList, accept="text/json")
def items_post(request):
    """method : POST

       content_type: text/json

       path : items

       body : Sequence of Item

       return codes: 200, 400
    """

    data = json.loads(request.body)
    models.transform_to_python_and_store(data["items"],
                                         "Item", "items", request)
    return {"status": "succeeded"}

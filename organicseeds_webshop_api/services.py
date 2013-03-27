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

items = Service(name='items',
                path='/items',
                description="Service to upload items")


def find_element(path, context):
    subpaths = path.split("/")
    ob = context
    for subpath in subpaths:
        ob = ob[subpath]
    return ob


@categories.post(schema=schemata.CategoriesList)
def categories_post(request):
    """method : POST

       path : categories

       body : json

       * categories : Sequence of Category

       return code: 200

       return error code: 400

    """
    data = json.loads(request.body)
    models.transform_to_python_and_store(data["categories"],
                                        "Category", "categories", request)
    return {"status": "succeeded"}

@item_groups.post(schema=schemata.ItemGroupsList)
def item_groups_post(request):
    """method : POST

       path : item_groups

       body : json

       * item_groups : Sequence of ItemGroup

       return code: 200

       return error code: 400

    """
    data = json.loads(request.body)
    models.transform_to_python_and_store(data["item_groups"],
                                         "ItemGroup", "item_groups", request)
    return {"status": "succeeded"}


@items.post(schema=schemata.ItemsList)
def items_post(request):
    """method : POST

       path : items

       body : json

       * unit_of_measures : Sequence of UnitOfMeasure
       * vpe_types : Sequence of VPEType
       * items : Sequence of Item

       return code: 200

       return error code: 400

    """

    data = json.loads(request.body)
    models.transform_to_python_and_store(data["items"],
                                         "Item", "items", request)
    models.transform_to_python_and_store(data["unit_of_measures"],
                                         "UnitOfMeasure", "unit_of_measures", request)
    models.transform_to_python_and_store(data["vpe_types"],
                                         "VPEType", "vpe_types", request)
    return {"status": "succeeded"}

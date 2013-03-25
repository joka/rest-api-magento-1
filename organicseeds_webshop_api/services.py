import json
import transaction
from pyramid.security import Everyone, Authenticated, Allow
from cornice import Service

from organicseeds_webshop_api import schemata
from organicseeds_webshop_api import models


categories = Service(name='categories',
                     path='/categories',
                     description="Service to upload webshop categories")
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
    data = json.loads(request.body)
    return {"test": "succeeded"}


@items.post(schema=schemata.ItemsList)
def items_post(request):
    data = json.loads(request.body)
    models.transform_to_python_and_store(data["items"],
                                         "Item", "items", request)
    models.transform_to_python_and_store(data["unit_of_measures"],
                                         "UnitOfMeasure", "unit_of_measures", request)
    models.transform_to_python_and_store(data["vpe_types"],
                                         "VPEType", "vpe_types", request)
    return {"test": "succeeded"}

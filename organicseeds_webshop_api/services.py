import json
import transaction
from pyramid.security import Everyone, Authenticated, Allow
from cornice import Service

from organicseeds_webshop_api.utilities import IContentRegistryUtility


from organicseeds_webshop_api import schemata


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
    contentregistry = request.registry.getUtility(IContentRegistryUtility)
    itemtype = contentregistry.get_content_type("Item")
    app_root = request.root.app_root
    items = app_root["items"]
    catalog = app_root.catalog
    document_map =  app_root.document_map
    for i in data["items"]:
        import ipdb; ipdb.set_trace()
        item = itemtype.deserialize(i)
        items[item.id] = "test"
        path = "categories/" + item.id
        catalog_id = document_map.add(path)
        catalog.index_doc(catalog_id, item)
    transaction.commit()
    return {"test": "succeeded"}

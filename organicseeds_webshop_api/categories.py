import json
from cornice import Service

from organicseeds_webshop_api import schemata

desc = """\
Service to upload webshop categories.
"""

categories = Service(name='categories', path='/categories', description=desc)
items = Service(name='items', path='/items', description=desc)


@categories.post(schema=schemata.CategoriesList)
def categories_post(request):
    data = json.loads(request.body)
    import ipdb; ipdb.set_trace()
    return {"test": "succeeded"}

@items.post(schema=schemata.ItemsList)
def items_post(request):
    data = json.loads(request.body)
    import ipdb; ipdb.set_trace()
    return {"test": "succeeded"}

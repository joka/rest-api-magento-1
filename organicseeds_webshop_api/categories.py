import string
from cornice.tests.support import CatchErrors
from colander import MappingSchema, SchemaNode, String
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from cornice import Service
from cornice.schemas import CorniceSchema

from organicseeds_webshop_api import schemata

desc = """\
Service to upload webshop categories.
"""

categories = Service(name='categories', path='/categories', description=desc)


@categories.post(schema=schemata.CategoriesList)
def categories_post(request):
    import pdb; pdb.set_trace()
    return {"test": "succeeded"}

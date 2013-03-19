
import string
from cornice.tests.support import CatchErrors
from colander import MappingSchema, SequenceSchema, SchemaNode, String
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from cornice import Service
from cornice.schemas import CorniceSchema

##############
# Attributes #
##############


##############
# Categories #
##############

class Category(MappingSchema):
    foo = SchemaNode(String(), location="body", type='str')
    bar = SchemaNode(String(), location="body", type='str')
    baz = SchemaNode(String(), location="body", type='str', required=False)

class Categories(SequenceSchema):
    category = Category()

class CategoriesList(MappingSchema):
    categories = Categories()

#########################
# Items (shop products) #
#########################





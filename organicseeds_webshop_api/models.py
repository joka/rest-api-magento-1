from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOBTree
from zope import interface
import transaction
from pyramid.security import Everyone, Authenticated, Allow
import limone_zodb
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap

from organicseeds_webshop_api import schemata
from organicseeds_webshop_api.utilities import IContentRegistryUtility


class Root(object):
    """Pyramid traversal root object"""

    __acl__ = [
        (Allow, Everyone, "view"),
        (Allow, Authenticated, "authenticated"),
        ]

    def __init__(self, request, app_root, app_root_id):
        self.request = request
        self.app_root = app_root
        self.app_root_id = app_root_id


class WebshopAPI(PersistentMapping):
    """ZODB database application root object"""


def bootstrap(zodb_root, app_root_id, request):
    """Setup Root Object and the ZODB Database structure"""

    if not app_root_id in zodb_root:
        # add root folders
        app_root = WebshopAPI()
        zodb_root[app_root_id] = app_root
        zodb_root[app_root_id]["categories"] = OOBTree()
        zodb_root[app_root_id]["item_groups"] = OOBTree()
        zodb_root[app_root_id]["items"] = OOBTree()
        zodb_root[app_root_id]["unit_of_measures"] = OOBTree()
        zodb_root[app_root_id]["vpe_types"] = OOBTree()
        # add repoze.catalog for indexing
        app_root.catalog = Catalog()
        app_root.catalog['parent_id'] = CatalogFieldIndex('parent_id')
        app_root.catalog['id'] = CatalogFieldIndex('id')
        app_root.catalog['__type__'] = CatalogFieldIndex('__type__')
        app_root.catalog['group'] = CatalogFieldIndex('group')
        app_root.catalog['vpe_type_id'] = CatalogFieldIndex('vpe_type_id')
        app_root.catalog['unit_of_measure_id'] = CatalogFieldIndex('unit_of_measure_id')
        app_root.catalog['quality_id'] = CatalogFieldIndex('quality_id')
        app_root.catalog['vpe_default'] = CatalogFieldIndex('vpe_default')
        app_root.document_map = DocumentMap()
        transaction.commit()
    return Root(request, zodb_root[app_root_id], app_root_id)


def includeme(config):
    """register limone content types"""
    # get content types registry
    contentregistry = config.registry.getUtility(IContentRegistryUtility)
    # add content types
    item = limone_zodb.make_content_type(schemata.Item, 'Item')
    contentregistry.register_content_type(item)
    unitofmeasure = limone_zodb.make_content_type(schemata.UnitOfMeasure, 'UnitOfMeasure')
    contentregistry.register_content_type(unitofmeasure)
    vpetype = limone_zodb.make_content_type(schemata.VPEType, 'VPEType')
    contentregistry.register_content_type(vpetype)
    itemgroup = limone_zodb.make_content_type(schemata.ItemGroup, 'ItemGroup')
    contentregistry.register_content_type(itemgroup)
    category = limone_zodb.make_content_type(schemata.Category, 'Category')
    contentregistry.register_content_type(category)


def transform_to_python_and_store(jsonlist, content_type, folder_id, request):
    contentregistry = request.registry.getUtility(IContentRegistryUtility)
    itemtype = contentregistry.get_content_type(content_type)
    app_root = request.root.app_root
    folder = app_root[folder_id]
    catalog = app_root.catalog
    document_map =  app_root.document_map
    # create object
    for i in jsonlist:
        # transform to python
        obj = itemtype.deserialize(i)
        # store in folder
        folder[obj.id] = "test"
        # catalog
        path = "%s/%s" % (folder_id, obj.id)
        catalog_id = document_map.add(path)
        catalog.index_doc(catalog_id, obj)
    # link objects
    transaction.commit()

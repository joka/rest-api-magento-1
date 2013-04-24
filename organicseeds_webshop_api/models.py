from copy import deepcopy
from persistent.mapping import PersistentMapping
from BTrees.OOBTree import OOBTree
import transaction
from pyramid.security import Everyone, Authenticated, Allow
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap


class Root(object):
    """Pyramid traversal root object"""

    __acl__ = [(Allow, Everyone, "view"),
               (Allow, Authenticated, "authenticated"),
               ]

    def __init__(self, request, app_root):
        self.request = request
        self.app_root = app_root


class WebshopAPI(PersistentMapping):
    """Application root object"""


class Folder(OOBTree):
    """Folder to store Entities"""


class Data(PersistentMapping):
    """Dictionary to store colander appstruct data"""

    def from_appstruct(self, appstruct):
        """"
        :param appstruct: Mapping to updated object data
        :type appstruct: Dictionary, keys are string, (colander appsctruct)
        """
        self.update(appstruct)

    def to_appstruct(self, appstruct):
        """"
        :rtype appstruct: Dictionary, keys are string, (colander appstruct)
        """
        appstruct = deepcopy(self.data)
        return appstruct


class Entity(Data):
    """Webshop entity"""

    __parent__ = None


class Category(Entity):
    """Webshop entity category"""


class ItemGroup(Entity):
    """Webshop entity item group"""


class Item(Entity):
    """Webshop entity item"""


class EntityData(Data):
    """Additional data for Entities"""


def get_id(obj, default):
    return obj.get("id", default)


def get_parent_id(obj, default):
    return obj.get("parent_id", default)


def get__type__(obj, default):
    return obj.get("__type__", default)


def get_group(obj, default):
    return obj.get("group", default)


def get_vpe_type_id(obj, default):
    return obj.get("vpe_type_id", default)


def get_unit_of_measure_id(obj, default):
    return obj.get("unit_of_measure_id", default)


def get_vpe_default(obj, default):
    return obj.get("vpe_default", default)


def get_quality_id(obj, default):
    return obj.get("vpe_default", default)


def bootstrap(zodb_root, app_root_id, request):
    """Setup Root Object and the ZODB Database structure"""

    if not app_root_id in zodb_root:
        # add root folders
        app_root = WebshopAPI()
        zodb_root[app_root_id] = app_root
        zodb_root[app_root_id]["categories"] = Folder()
        zodb_root[app_root_id]["item_groups"] = Folder()
        zodb_root[app_root_id]["items"] = Folder()
        zodb_root[app_root_id]["unit_of_measures"] = Folder()
        zodb_root[app_root_id]["vpe_types"] = Folder()
        # add repoze.catalog for indexing
        app_root["catalog"] = Catalog()
        app_root["catalog"]['parent_id'] = CatalogFieldIndex(get_parent_id)
        app_root["catalog"]['id'] = CatalogFieldIndex(get_id)
        app_root["catalog"]['__type__'] = CatalogFieldIndex(get__type__)
        app_root["catalog"]['group'] = CatalogFieldIndex(get_group)
        app_root["catalog"]['vpe_type_id'] = CatalogFieldIndex(get_vpe_type_id)
        app_root["catalog"]['unit_of_measure_id'] = \
            CatalogFieldIndex(get_unit_of_measure_id)
        app_root["catalog"]['quality_id'] = CatalogFieldIndex(get_quality_id)
        app_root["catalog"]['vpe_default'] = CatalogFieldIndex(get_vpe_default)
        app_root["document_map"] = DocumentMap()
        transaction.commit()
    return Root(request, zodb_root[app_root_id])


def includeme(config):
    """register limone content types"""
    # get content types registry
    #contentregistry = config.registry.getUtility(IContentRegistryUtility)


def transform_to_python_and_store(data, itemtype, data_key, request):
    app_root = request.root.app_root
    folder = app_root[data_key]
    catalog = app_root["catalog"]
    document_map = app_root["document_map"]
    appstructs = data[data_key]
    for appstruct in appstructs:
        obj_id = appstruct["id"]
        obj = None
        # create and store object if not existing
        if obj_id not in folder:
            obj = itemtype()
            obj.from_appstruct(appstruct)
            folder[obj_id] = obj
        # updated existing object
        else:
            obj = folder[obj_id]
            obj.from_appstruct(appstruct)
        # catalog object
        obj_path = "%s/%s" % (data_key, obj_id)
        catalog_id = document_map.add(obj_path)
        catalog.index_doc(catalog_id, obj)
        #link parent
        if "parent_id" in obj:
            parent_id = obj["parent_id"]
            if data_key == "items":
                category_parent = app_root["categories"].get(parent_id, None)
                item_group_parent = \
                    app_root["item_groups"].get(parent_id, None)
                obj.__parent__ = category_parent or item_group_parent
            if data_key in ["item_groups", "categories"]:
                category_parent = app_root["categories"].get(parent_id, None)
                obj.__parent__ = category_parent


def delete(data, itemtype, data_key, request):
    app_root = request.root.app_root
    folder = app_root[data_key]
    catalog = app_root["catalog"]
    document_map = app_root["document_map"]
    # uncatalog
    for i in folder.iterkeys():
        obj_path = "%s/%s" % (data_key, i)
        catalog_id = document_map.docid_for_address(obj_path)
        catalog.unindex_doc(catalog_id)
    # delete objects
    folder.clear()

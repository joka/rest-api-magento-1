from copy import deepcopy
from persistent.mapping import PersistentMapping
from persistent.list import PersistentList
from BTrees.OOBTree import OOBTree
import transaction
from pyramid.security import Everyone, Authenticated, Allow
from pyramid.location import lineage
from repoze.catalog.indexes.field import CatalogFieldIndex
from repoze.catalog.indexes.keyword import CatalogKeywordIndex
from repoze.catalog.catalog import Catalog
from repoze.catalog.document import DocumentMap

from organicseeds_webshop_api.url_normalizer import url_normalizer
from organicseeds_webshop_api.schemata import attributes_with_inheritance

#################################
#  Pyramid routing root object  #
#################################


class Root(object):
    """Pyramid traversal root object"""

    __acl__ = [(Allow, Everyone, "view"),
               (Allow, Authenticated, "authenticated"),
               ]

    def __init__(self, request, app_root):
        self.request = request
        self.app_root = app_root


######################################
#  Models to store webshop entities  #
######################################


def _translate(data, lang):
    if not isinstance(data, dict):
        return data
    for key in data:
        if isinstance(data[key], dict):
            value = data[key].get(lang, None)\
                or data[key].get("default", None)\
                or data[key]
            data[key] = value
        if isinstance(data[key], list):
            for i in data[key]:
                _translate(i, lang)
    return data


def _add_inherited_attributes(entity, attributename):
    entities = [x for x in lineage(entity)]
    attribute_values = []
    attribute_ids = set()
    for e in entities:
        attrs = deepcopy(e.get(attributename, []))
        for a in attrs:
            if a["id"] not in attribute_ids:
                attribute_ids.add(a["id"])
                attribute_values.append(a)
    return attribute_values


class WebshopAPI(PersistentMapping):
    """Application root object"""


class Folder(OOBTree):
    """Folder to store Entities"""


class Data(PersistentMapping):
    """Dictionary to store colander appstruct data"""

    def __init__(self, appstruct={}):
        super(Data, self).__init__()
        self.from_appstruct(appstruct)

    def from_appstruct(self, appstruct):
        """"
        :param appstruct: Mapping to updated object data
        :type appstruct: Dictionary, keys are string, (colander appsctruct)
        """
        self.update(appstruct)

    def to_data(self, lang=None):
        """"
        :return dictionary with all data
        """
        data = deepcopy(self.data)
        if lang:
            data = _translate(data, lang)
        return data


class Entity(Data):
    """Webshop entity"""

    __parent__ = None
    webshop_id = 0
    url_slugs = {}

    def __init__(self, appstruct={}):
        super(Entity, self).__init__(appstruct)
        self.url_slugs = PersistentMapping()


class Category(Entity):
    """Webshop entity category"""

    __children__ = []

    def __init__(self, appstruct={}):
        super(Category, self).__init__(appstruct)
        self.__children__ = PersistentList()


class ItemGroup(Entity):
    """Webshop entity item group"""

    __children__ = []

    def __init__(self, appstruct={}):
        super(ItemGroup, self).__init__(appstruct)
        self.__children__ = PersistentList()

    def to_data(self, lang=None, with_children=False, children_shop_id=""):
        """"
        :return dictionary with all data
        """
        data = deepcopy(self.data)
        for key in attributes_with_inheritance:
            data[key] = _add_inherited_attributes(self, key)
        if lang:
            data = _translate(data, lang)
        children = deepcopy(self.__children__)
        if children_shop_id:
            children = [x for x in children \
                        if (children_shop_id, True) in x["shops"]
                        or [children_shop_id, True] in x["shops"]]
        if with_children:
            data["children_vpe_types"] = {}
            data["children_qualities"] = {}
            data["children_grouped"] = {}
            for child in children:
                child_ = child.to_data(lang)
                vpe = child_["vpe_type"]
                vpe_id = vpe["id"]
                quality = child_["quality"]
                quality_id = quality["id"]
                if vpe_id not in data["children_grouped"]:
                    data["children_grouped"][vpe_id] = {}
                    data["children_vpe_types"][vpe_id] = vpe
                del(child_["vpe_type"])
                if quality_id not in data["children_grouped"][vpe_id]:
                    data["children_grouped"][vpe_id][quality_id] = {}
                    data["children_qualities"][quality_id] = quality
                del(child_["quality"])
                data["children_grouped"][vpe_id][quality_id][child_["sku"]] =\
                    child_
        return data


class Item(Entity):
    """Webshop entity item"""

    unit_of_measure = None
    vpe_type = None
    quality = None

    def to_data(self, lang=None):
        """"
        :return dictionary with all data
        """
        data = deepcopy(self.data)
        if lang:
            data = _translate(data, lang)
        if self.vpe_type:
            data["vpe_type"] = self.vpe_type.to_data(lang)
        if self.unit_of_measure:
            data["unit_of_measure"] = self.unit_of_measure.to_data(lang)
        if self.quality:
            data["quality"] = _translate(self.quality, lang)
        data["webshop_id"] = self.webshop_id
        return data


class EntityData(Data):
    """Additional data for Entities"""


##################################
#  Helpers to index entity data  #
##################################


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
    return obj.get("quality_id", default)


def get_title_url_slugs(obj, default):
    keywords = default
    title = obj.get("title", None)
    if title:
        keywords = [url_normalizer(t) for t in title.values()]
    return keywords


##################################
#  Create basic data sctructure  #
##################################


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
        app_root["catalog"]['title_url_slugs'] = CatalogKeywordIndex(
            get_title_url_slugs)
        app_root["document_map"] = DocumentMap()
        transaction.commit()
    return Root(request, zodb_root[app_root_id])

from repoze.catalog.query import (
    Eq,
    And,
    Or,
)

from organicseeds_webshop_api import url_normalizer
from organicseeds_webshop_api.exceptions import _500

#####################################
#  Helpers to create/delete models  #
#####################################


def store(appstructs, itemtype, data_key, request):
    entities = []
    app_root = request.root.app_root
    folder = app_root[data_key]
    catalog = app_root["catalog"]
    document_map = app_root["document_map"]
    for appstruct in appstructs:
        obj_id = appstruct["id"]
        obj = None
        # create and store object if not existing
        if obj_id not in folder:
            obj = itemtype()
            obj.from_appstruct(appstruct)
            folder[obj_id] = obj
            entities.append(obj)
        # updated existing object
        else:
            obj = folder[obj_id]
            obj.from_appstruct(appstruct)
        # catalog object
        obj_path = "%s/%s" % (data_key, obj_id)
        catalog_id = document_map.add(obj_path)
        catalog.index_doc(catalog_id, obj)
        #link parent (child -> parent)
        parent_id = obj.get("parent_id", None)
        if parent_id:
            category_parent = app_root["categories"].get(parent_id, None)
            item_group_parent = app_root["item_groups"].get(parent_id, None)
            parent = category_parent or item_group_parent
            if parent is not None:
                obj.__parent__ = parent
                children = parent.__children__
                if obj not in children:
                    children.append(obj)
        # update link parent (parent -> child)
        if hasattr(obj, "__children__"):
            result = catalog.query(Eq('parent_id', obj["id"]))
            for docid in result[1]:
                item = docid_to_entity(docid, request)
                if item:
                    children = obj.__children__
                    if obj not in children:
                        item.__parent__ = obj
                        children.append(item)
        # link item vpe type
        vpe_type_id = obj.get("vpe_type_id", None)
        if vpe_type_id:
            obj.vpe_type = app_root["vpe_types"].get(vpe_type_id, None)
        # link item unit_of_measure
        unit_of_measure = obj.get("unit_of_measure_id", None)
        if unit_of_measure:
            obj.unit_of_measure = app_root["unit_of_measures"].get(
                unit_of_measure, None)
        # link item quality (child -> parent)
        quality_id = obj.get("quality_id", None)
        if quality_id and obj.__parent__:
            qualities = obj.__parent__["qualities"]
            try:
                quality = [q for q in qualities if q["id"] == quality_id][0]
            except IndexError:
                error = "Item %s has non existing quality %s"
                raise _500(msg=error % (obj["id"], quality_id))
            obj.quality = quality
        # update link item quality (parent -> child)
        qualities = obj.get("qualities", None)
        if qualities:
            for i in obj.__children__:
                try:
                    quality = [q for q in qualities
                               if q["id"] == i["quality_id"]][0]
                    i.quality = quality
                except IndexError:
                    error = "Child %s of %s has non existing quality_id"
                    raise _500(msg=error % (i["id"], obj["id"]))
    return entities


def docid_to_entity(docid, request):
    """returns the entity mapped to the repoze.catalog docid
    """
    entity = None
    app_root = request.root.app_root
    document_map = app_root["document_map"]
    address = document_map.address_for_docid(docid)
    if address:
        folder, key = folder, key = address.split("/")
        entity = app_root.get(folder).get(key)
    return entity


def delete(appstructs, data_key, request):
    app_root = request.root.app_root
    folder = app_root[data_key]
    catalog = app_root["catalog"]
    document_map = app_root["document_map"]
    for i in [a["id"] for a in appstructs]:
        # uncatalog
        obj_path = "%s/%s" % (data_key, i)
        catalog_id = document_map.docid_for_address(obj_path)
        catalog.unindex_doc(catalog_id)
        # delete objects
        if i in folder:
            item = folder[i]
            parent = item.__parent__
            if parent is not None:
                parent.__children__.remove(item)
                item.__parent__ = None
            del(folder[i])


def delete_all(data_key, request):
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


def remove_none_values(appstructs):
    for item in appstructs:
        for i, v in item.items():
            if v is None:
                del(item[i])
    return appstructs


def set_webshop_ids(items, webshop_ids):
    for item, webshop_id in zip(items, webshop_ids):
        item.webshop_id = webshop_id


def get_entities_item_children(entities, request):
    items_webshop_ids = []
    items = []
    for entity in entities:
        for child in entity.__children__:
            items.append(child)
            items_webshop_ids.append(child.webshop_id)
    return items_webshop_ids, items


def get_url_slug(title, unique_suffix, request):
    catalog = request.root.app_root["catalog"]
    url_slug = url_normalizer.url_normalizer(title)
    existing = catalog.query(Eq('title_url_slugs', url_slug))[0]
    if existing >= 1:
        url_slug += unique_suffix
    return url_slug


def search(request, operator="AND", **kwargs):
    assert operator in ["AND", "OR"]
    catalog = request.root.app_root["catalog"]
    connector = And if operator == "AND" else Or
    queries = []
    results = []
    for k,v in kwargs.items():
        queries.append(Eq(k, v))
    if queries:
        result_set = catalog.query(connector(*queries))[1]
        for docid in result_set:
            entity = docid_to_entity(docid, request)
            results.append(entity)
    return results


#def find_element(path, context):
    #subpaths = path.split("/")
    #ob = context
    #for subpath in subpaths:
        #ob = ob[subpath]
    #return ob

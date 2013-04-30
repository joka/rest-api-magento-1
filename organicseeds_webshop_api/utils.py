
#####################################
#  Helpers to create/delete models  #
#####################################


def store(appstructs, itemtype, data_key, request):
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


#def find_element(path, context):
    #subpaths = path.split("/")
    #ob = context
    #for subpath in subpaths:
        #ob = ob[subpath]
    #return ob

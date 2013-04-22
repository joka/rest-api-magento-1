
###################
# base validators #
###################


def validate_id_does_not_exists(data_key, request):
    entities = request.validated[data_key]
    entity_ids = set([i["id"] for i in entities])
    app_root = request.root.app_root
    existing_folder = app_root[data_key]
    existing = set(existing_folder.keys())
    already_exists = existing.intersection(entity_ids)

    error = 'The following ids do already exists in %s: %s'
    if already_exists:
        request.errors.add('body', 'id',
                           error % (data_key,
                                    [x for x in already_exists].__str__()))


def validate_id_does_exists(data_key, request):
    entities = request.validated[data_key]
    entity_ids = set([i["id"] for i in entities])
    app_root = request.root.app_root
    existing_folder = app_root[data_key]
    existing = set(existing_folder.keys())
    not_existing = entity_ids.difference(existing)

    error = 'The following ids do not exists in %s: %s'
    if not_existing:
        request.errors.add('body', 'id',
                           error % (data_key,
                                    [x for x in not_existing].__str__()))


def validate_no_reference_ids_exist(data_key, data_key_refs,
                                    attr_ref_id, request):
    app_root = request.root.app_root
    entity_ids = app_root[data_key].keys()
    entity_refs = app_root[data_key_refs].values()
    entity_refs_ids = [x[attr_ref_id] for x in entity_refs]

    existing_references = set(entity_refs_ids).intersection(set(entity_ids))

    error = 'The following %s are still referenced in %s: %s'
    if existing_references:
        request.errors.add('body', data_key_refs,
                           error % (data_key, data_key_refs,
                                    [x for x in existing_references].__str__())
                           )
#######################
# /categories service #
#######################


def validate_category_id_does_not_exists(request):
    validate_id_does_not_exists("categories", request)


def validate_category_id_does_exists(request):
    validate_id_does_exists("categories", request)


def validate_category_parent_id(request):
    categories = request.validated["categories"]
    new_ids = [i["id"] for i in categories]
    app_root = request.root.app_root
    existing_ids = [x for x in app_root["categories"].keys()]
    for i in categories:
        cid = i["id"]
        parent_id = i["parent_id"]
        if cid == parent_id:
            # Note: circle structures are not detected
            error = 'parent_id: %s and id: %s are the same' % (parent_id, cid)
            request.errors.add('body', 'parent_id', error)
        if parent_id is None:
            continue
        if parent_id not in new_ids + existing_ids:
            error = "parent_id: %s of category: %s does not exists"\
                    " and is not going to be created" % (parent_id, cid)
            request.errors.add('body', 'parent_id', error)


def validate_no_item_group_references_exist(request):
    validate_no_reference_ids_exist("categories", "item_groups",
                                    "parent_id", request)

########################
# /item_groups service #
########################


def validate_item_group_id_does_not_exists(request):
    validate_id_does_not_exists("item_groups", request)


def validate_item_group_parent_id(request):
    item_groups = request.validated["item_groups"]
    item_group_parent_ids = set([i["parent_id"] for i in item_groups])
    app_root = request.root.app_root
    existing = set(app_root["categories"].keys())
    non_existing = item_group_parent_ids.difference(existing)

    error = 'The following parent_ids do no exists in categories: %s'
    if non_existing:
        request.errors.add('body', 'parent_id',
                           error % ([x for x in non_existing].__str__()))


def validate_item_group_no_item_references_exist(request):
    validate_no_reference_ids_exist("item_groups", "items",
                                    "parent_id", request)

#############################
# /unit_of_measures service #
#############################


def validate_unit_of_measure_id_does_not_exists(request):
    validate_id_does_not_exists("unit_of_measures", request)


def validate_unit_of_measure_no_item_references_exist(request):
    validate_no_reference_ids_exist("unit_of_measures", "items",
                                    "unit_of_measure_id", request)


######################
# /vpe_types service #
######################


def validate_vpe_type_id_does_not_exists(request):
    validate_id_does_not_exists("vpe_types", request)


def validate_vpe_type_no_item_references_exist(request):
    validate_no_reference_ids_exist("vpe_types", "items",
                                    "vpe_type_id", request)

##################
# /items service #
##################


def validate_item_id_does_not_exists(request):
    validate_id_does_not_exists("items", request)


def validate_item_id_does_exists(request):
    validate_id_does_exists("items", request)


def validate_item_parent_id(request):
    items = request.validated["items"]
    item_parent_ids = set([i["parent_id"] for i in items])
    app_root = request.root.app_root
    categories = set(app_root["categories"].keys())
    item_groups = set(app_root["item_groups"].keys())
    existing = set.union(categories, item_groups)
    non_existing = item_parent_ids.difference(existing)

    error = 'The following parent_ids do no exists in item_groups '\
            '"or categories: %s'
    if non_existing:
        request.errors.add('body', 'parent_id',
                           error % ([x for x in non_existing].__str__()))


def validate_item_vpe_type_id(request):
    items = request.validated["items"]
    item_vpe_type_ids = set([i["vpe_type_id"] for i in items])
    app_root = request.root.app_root
    existing = set(app_root["vpe_types"].keys())
    non_existing = item_vpe_type_ids.difference(existing)

    error = 'The following vpe_type_ids do no exists in vpe_types: %s'
    if non_existing:
        request.errors.add('body', 'vpe_type_id',
                           error % ([x for x in non_existing].__str__()))


def validate_item_unit_of_measure_id(request):
    items = request.validated["items"]
    item_unit_of_measure_ids = set([i["unit_of_measure_id"] for i in items])
    app_root = request.root.app_root
    existing = set(app_root["unit_of_measures"].keys())
    non_existing = item_unit_of_measure_ids.difference(existing)

    error = 'The following unit_of_measure_ids do no exists '\
            'in unit_of_measures: %s'
    if non_existing:
        request.errors.add('body', 'unit_of_measur_id',
                           error % ([x for x in non_existing].__str__()))

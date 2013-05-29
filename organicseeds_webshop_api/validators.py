from collections import Counter

###################
# base validators #
###################


def validate_key_unique(data_key, key, request):
    appstructs = request.validated[data_key]
    values = [x[key] for x in appstructs if key in x]
    values_nonunique = [x for x, y in Counter(values).items() if y > 1]

    error = 'The following %s are not unique: %s'
    if values_nonunique:
        request.errors.add('body', key, error % (key, str(values_nonunique)))


def validate_key_does_not_exists(data_key, key, request):
    appstructs = request.validated[data_key]
    values = set([i[key] for i in appstructs if key in i])
    existing_folder = request.root.app_root[data_key]
    existing = set([x[key] for x in existing_folder.values() if key in x])
    already_exists = existing.intersection(values)

    error = 'The following %s do already exists in %s: %s'
    if already_exists:
        request.errors.add('body', key,
                           error % (key, data_key,
                                    [x for x in already_exists].__str__()))


def _expand_titles(appstructs):
    titles = [x["title"] for x in appstructs if x.get("title", None)]
    for x in titles:
        if "default" in x:
            yield x["default"]
        if "fr" in x:
            yield x["fr"]
        if "en" in x:
            yield x["en"]
        if "it" in x:
            yield x["it"]
        if "de" in x:
            yield x["de"]


def validate_title_unique(data_key, request):
    appstructs = request.validated[data_key]
    titles = _expand_titles(appstructs)
    titles = [x for x in titles if x]
    titles_nonunique = [x for x, y in Counter(titles).items() if y > 1]

    error = 'The following titles are not unique: %s'
    if titles_nonunique:
        request.errors.add('body', "title", error % (str(titles_nonunique)))


def validate_title_does_not_exists(data_key, request):
    appstructs = request.validated[data_key]
    titles = _expand_titles(appstructs)
    existing_folder = request.root.app_root[data_key]
    existing_titles = set(_expand_titles([x for x in
                                          existing_folder.values()]))
    already_exists = existing_titles.intersection(titles)

    error = 'The following titles do already exists in %s: %s'
    if already_exists:
        request.errors.add('body', "title", error % (data_key,
                           [x for x in already_exists].__str__()))


def validate_id_does_not_exists(data_key, request):
    entities = request.validated[data_key]
    entity_ids = set([i["id"] for i in entities])
    existing_folder = request.root.app_root[data_key]
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
    existing_folder = request.root.app_root[data_key]
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


def validate_category_id_unique(request):
    validate_key_unique("categories", "id", request)


def validate_category_id_does_exists(request):
    validate_id_does_exists("categories", request)


def validate_category_id_does_not_exists(request):
    validate_id_does_not_exists("categories", request)


def validate_category_title_unique(request):
    validate_title_unique("categories", request)


def validate_category_title_does_not_exists(request):
    validate_title_does_not_exists("categories", request)


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


def validate_item_group_id_unique(request):
    validate_key_unique("item_groups", "id", request)


def validate_item_group_id_does_not_exists(request):
    validate_id_does_not_exists("item_groups", request)


def validate_item_group_title_unique(request):
    validate_title_unique("item_groups", request)


def validate_item_group_title_does_not_exists(request):
    validate_title_does_not_exists("item_groups", request)


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


def validate_unit_of_measure_id_unique(request):
    validate_key_unique("unit_of_measures", "id", request)


def validate_unit_of_measure_id_does_not_exists(request):
    validate_id_does_not_exists("unit_of_measures", request)


def validate_unit_of_measure_id_does_exists(request):
    validate_id_does_exists("unit_of_measures", request)


def validate_unit_of_measure_no_item_references_exist(request):
    validate_no_reference_ids_exist("unit_of_measures", "items",
                                    "unit_of_measure_id", request)


######################
# /vpe_types service #
######################


def validate_vpe_type_id_unique(request):
    validate_key_unique("vpe_types", "id", request)


def validate_vpe_type_id_does_not_exists(request):
    validate_id_does_not_exists("vpe_types", request)


def validate_vpe_type_id_does_exists(request):
    validate_id_does_exists("vpe_types", request)


def validate_vpe_type_no_item_references_exist(request):
    validate_no_reference_ids_exist("vpe_types", "items",
                                    "vpe_type_id", request)

##################
# /items service #
##################


def validate_items_id_unique(request):
    validate_key_unique("items", "id", request)


def validate_items_id_does_not_exists(request):
    validate_id_does_not_exists("items", request)


def validate_items_sku_unique(request):
    validate_key_unique("items", "sku", request)


def validate_items_sku_does_not_exists(request):
    validate_key_does_not_exists("items", "sku", request)


def validate_items_title_unique(request):
    validate_title_unique("items", request)


def validate_items_title_does_not_exists(request):
    validate_title_does_not_exists("items", request)


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


############
#  search  #
############


def validate_search_parameters(request):
    parameters = request.GET
    request.validated = {}
    catalog = request.root.app_root["catalog"]
    allowed_search_keywords = catalog.keys() + ["lang", "operator"]
    if "lang" not in parameters:
        parameters["lang"] = "default"
    if "operator" not in parameters:
        parameters["operator"] = "AND"
    if parameters["operator"] not in ["AND", "OR"]:
        error = 'The operator value %s is not in ["AND", "OR"]'
        request.errors.add('querystring', 'operator',
                           error % (parameters["operator"]))
    for key in parameters:
        if key not in allowed_search_keywords:
            error = 'The search key %s is not in allowed.'\
                    'Valid search parameters are %s.'
            request.errors.add('querystring', key,
                               error % (key, allowed_search_keywords))
    if not request.errors:
        request.validated.update(parameters)

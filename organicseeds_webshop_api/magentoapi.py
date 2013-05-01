"""Module to mange the magento soap api"""
from __future__ import absolute_import
from xmlrpclib import Fault
import magento.api
import magento

from organicseeds_webshop_api import schemata
from organicseeds_webshop_api import url_normaliser


rpc_user = u"webshop_api"
rpc_secret = u"oxXCcvIAhdXcw"
apiurl = "http://hobby.developlocal.sativa.jokasis.de/"


#############
#  helpers  #
#############


def get_storeviews(appstruct):
    storeviews = []
    name_tmpl = "%s_%s_%s"
    for shop, enabled in appstruct.get("shops", []):
        type_ = shop[3:]
        country = shop[:2]
        lang = country
        if country == "ch":
            for lang in ["de", "fr", "it"]:
                name = name_tmpl % (lang, country, type_)
                storeviews.append((name, enabled, lang, country))
        else:
            name = name_tmpl % (lang, country, type_)
            storeviews.append((name, enabled, lang, country))
    return storeviews


def get_category_ids(data, request):
    """returns category magento ids of item data"""
    categories = request.root.app_root["categories"]
    category_ids = data.get("category_ids") or []
    category_webshop_ids = []
    for cat in category_ids:
        if cat in categories:
            webshop_id = categories[cat].webshop_id
            if webshop_id != 0:
                category_webshop_ids.append(webshop_id)
    return category_webshop_ids


def get_website_ids(data):
    """returns item data specific website ids"""
    shops = [shop[0] for shop in data["shops"] if shop[1]]
    website_ids = set()
    for shop in shops:
        shop_lang = shop[:2]
        website_name = u"%s_website" % (shop_lang)
        website_ids.add(website_name)
    return [w for w in website_ids]


def get_all_website_ids():
    """returns all magento website ids"""
    schema = schemata.WebsiteID()
    return schema.validator.choices


def get_translation(data, key, lang):
    """returns translation of data[key] or None"""
    return data.get(key) and data[key].get(lang, None) or None


def get_website_value(appstruct, key, country):
    websites = appstruct.get(key, [])
    website_id = country + "_website"
    values = [x[1] for x in websites if x[0] == website_id]
    value = values and values[0] or None
    return value

#def get_magento_inventory_status(data):
    #status = data["inventory_status"]
    #magento_status = 1 if status == 2 else 0
    #return magento_status


##############################
#  magento api proxies       #
##############################

class MagentoAPI(magento.api.API):

    entity_data_key = u""
    magento_type = u""
    magento_method = u""

    items = None
    item_groups = None
    categories = None
    entities = None

    def __init__(self, request):
        super(MagentoAPI, self).__init__(apiurl, rpc_user, rpc_secret)
        self.request = request
        self.items = request.root.app_root["items"]
        self.categories = request.root.app_root["categories"]
        self.item_groups = request.root.app_root["item_groups"]
        self.entities = getattr(self, self.entity_data_key, [])

    def single_call(self, resource_path, arguments=[]):
        """Send magento api v.1 call"""
        return self.call(resource_path, arguments)

    def multi_call(self, calls):
        """Send magento api v.1 multiCall"""
        # slice calls to make magento happy and send
        results = []
        for i in range(0, len(calls), 8):
            calls_chunk = calls[i:i + 8]
            results_chunk = self.multiCall(calls_chunk)
            results += results_chunk
        # raise error if something went wrong
        for res in results:
            if isinstance(res, dict) and "faultCode" in res:
                raise Exception(res["faultCode"] + res["faultMessage"])
        return results

    def delete(self, appstructs):
        calls = []
        for data in appstructs:
            entity_id = data["id"]
            webshop_id = self.entities[entity_id].webshop_id
            calls.append([self.magento_method + "delete", [webshop_id]])
        return [bool(x) for x in self.multi_call(calls)]

    def delete_all(self):
        """to be implemented in subclass"""
        pass

    def create(self, appstructs):
        calls = []
        for appstruct in appstructs:
            calls.append([self.magento_method + 'create',
                          self._create_arguments(appstruct)])
        webshop_ids = [int(x) for x in self.multi_call(calls)]
        return webshop_ids

    def update(self, appstructs):
        calls = []
        for appstruct in appstructs:
            entity_id = appstruct["id"]
            webshop_id = self.entities[entity_id].webshop_id
            calls.append(
                [self.magento_method + 'update',
                 [webshop_id,
                  self._to_update_data(appstruct),
                  ]
                 ])
        results = [bool(x) for x in self.multi_call(calls)]
        return results

    def update_shops(self, webshop_ids, appstructs):
        calls = []
        for webshop_id, appstruct in zip(webshop_ids, appstructs):
            storeviews = get_storeviews(appstruct)
            for storeviewname, enabled, lang, country in storeviews:
                data = self._to_update_shops_data(appstruct, lang, country)
                if enabled:
                    data["visibility"] = 4
                else:
                    data["visibility"] = 1
                if data:
                    calls.append([self.magento_method + 'update',
                                  [webshop_id, data, storeviewname]])
        return self.multi_call(calls)

    def link_item_parents(self, webshop_ids, appstructs):
        calls = []
        for webshop_id, appstruct in zip(webshop_ids, appstructs):
            parent_id = appstruct["parent_id"]
            if parent_id in self.item_groups:
                parent_webshop_id = self.item_groups[parent_id].webshop_id
                calls.append(["catalog_product_link.assign",
                              ["grouped", parent_webshop_id, webshop_id]])
            if parent_id in self.categories:
                parent_webshop_id = self.categories[parent_id].webshop_id
                calls.append(['catalog_category.assignProduct',
                              [parent_webshop_id, webshop_id]])
        self.multi_call(calls)

    def link_category_parents(self, webshop_ids, appstructs):
        calls = []
        for webshop_id, appstruct in zip(webshop_ids, appstructs):
            parent_id = appstruct["parent_id"]
            if parent_id:
                parent_webshop_id = self.categories[parent_id].webshop_id
                calls.append(['catalog_category.move',
                              [webshop_id, parent_webshop_id]])
        self.multi_call(calls)

    def _create_arguments(self, appstruct):
        """to be implemented in subclass"""
        pass

    def _to_update_data(self, appstruct):
        """to be implemented in subclass"""
        pass

    def _to_update_shops_data(self, appstruct, lang, country="default"):
        """to be implemented in subclass"""

    def _to_create_data(self, appstruct):
        """to be implemented in subclass"""
        pass


class Items(MagentoAPI):

    entity_data_key = u"items"
    magento_type = u"simple"
    magento_method = u"catalog_product."

    def delete_all(self):
        webshop_entities = self.single_call(
            self.magento_method + "list",
            [{'type':{'ilike': self.magento_type}}])
        webshop_ids = [x["product_id"] for x in webshop_entities]
        calls = []
        for webshop_id in webshop_ids:
            calls.append([self.magento_method + "delete", [webshop_id]])
        self.multi_call(calls)

    def _create_arguments(self, appstruct):
        return [self.magento_type,
                4,  # attribute set
                appstruct["sku"],
                self._to_create_data(appstruct)]

    def _to_create_data(self, appstruct):
        """transforms item data to magento create data dictionary"""
        data = self._to_update_data(appstruct)
        data["status"] = 1  # global status is "enabled" for all websites
        data["visibility"] = 1  # global visibility is disabled
        data["websites"] = get_all_website_ids()  # enabled for all websites
        return data

    def _to_update_data(self, appstruct):
        """transforms item appstruct to magento update appstruct dictionary"""
        data = self._to_update_shops_data(appstruct, "default")
        extradata_tuples = [
            ("weight", appstruct.get("weight_brutto", None)),
            ("tax_class_id", appstruct.get("tax_class", None))]
            #"tier_price": get_tier_prices(item),
            #"stock_appstruct": get_stock_appstruct(item),
        data.update(dict([x for x in extradata_tuples if x[1] is not None]))
        return data

    def _to_update_shops_data(self, appstruct, lang, country="default"):
        """transforms item appstruct to magento update appstruct dictionary.
           returns only StringTranslation values
        """
        name = get_translation(appstruct, "title", lang)
        url_key = url_normaliser.url_normalizer(name) if name else None
        data_tuples = [
            ("name", name),
            ("url_key", url_key),
            ("description", get_translation(appstruct, "description", lang)),
            ("short_description", get_translation(appstruct,
                                                  "shortdescription", lang)),
            ("price", get_website_value(appstruct, "price", country))]
        return dict([x for x in data_tuples if x[1] is not None])


class ItemGroups(Items):

    entity_data_key = u"item_groups"
    magento_type = u"grouped"
    magento_method = u"catalog_product."

    def _create_arguments(self, appstruct):
        return [self.magento_type,
                4,  # attribute set
                appstruct["id"],  # pseudo sku
                self._to_create_data(appstruct)]


class Categories(MagentoAPI):

    entity_data_key = u"categories"
    magento_type = u"category"
    magento_method = u"catalog_category."

    def delete_all(self):
        if self.magento_method:
            results1 = self.single_call(self.magento_method + "level",
                                        [None, None, 1])
            results2 = self.single_call(self.magento_method + "level",
                                        [None, None, 2])
            results3 = self.single_call(self.magento_method + "level",
                                        [None, None, 3])
            results4 = self.single_call(self.magento_method + "level",
                                        [None, None, 4])
            webshop_ids = [int(x["category_id"]) for x in results1 + results2 +
                           results3 + results4]
            for webshop_id in webshop_ids:
                if webshop_id > 1:
                    try:
                        self.single_call(self.magento_method + "delete",
                                         [webshop_id])
                    except Fault:
                        pass

    def _create_arguments(self, appstruct):
        return [2,  # set parent to default root category
                self._to_create_data(appstruct)]

    def _to_create_data(self, appstruct):
        """transforms item data to magento create data dictionary"""
        data = self._to_update_data(appstruct)
        data["available_sort_by"] = ["position", "name", "price"]
        data["default_sort_by"] = "position"
        data["include_in_menu"] = 1
        data["is_active"] = 0
        return data

    def _to_update_data(self, appstruct):
        """transforms category appstruct to magento update data"""
        data = self._to_update_shops_data(appstruct, "default")
        extradata_tuples = []
        data.update(dict([x for x in extradata_tuples if x[1] is not None]))
        return data

    def _to_update_shops_data(self, appstruct, lang, country="default"):
        """transforms item appstruct to magento update appstruct dictionary.
           returns only StringTranslation values
        """
        name = get_translation(appstruct, "title", lang)
        url_key = url_normaliser.url_normalizer(name) if name else None
        data_tuples = [("name", name),
                       ("url_key", url_key),
                       ("short_description",
                        get_translation(appstruct, "shortdescription", lang)),
                       ]
        return dict([x for x in data_tuples if x[1] is not None])

# todo docu inventory status
# todo validate unique title, sku(items and item_groups), id

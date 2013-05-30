"""Module to mange the magento soap api"""
from __future__ import absolute_import
import subprocess
from xmlrpclib import Fault
import magento.api
import magento

from organicseeds_webshop_api import exceptions
from organicseeds_webshop_api import schemata
from organicseeds_webshop_api import utils


##############################
# magento api proxy helpers  #
##############################


def indexing_enable_manual(request):
    magento_whiz_script = request.registry.settings.get('magento_whiz_script')
    response = subprocess.check_output([magento_whiz_script,
                                        "indexer-manual", "all"])
    return response


def indexing_reindex(request):
    magento_whiz_script = request.registry.settings.get('magento_whiz_script')
    response = subprocess.check_output([magento_whiz_script,
                                        "indexer-reindex", "all"])
    return response


def indexing_enable_auto(request):
    magento_whiz_script = request.registry.settings.get('magento_whiz_script')
    response = subprocess.check_output([magento_whiz_script,
                                        "indexer-realtime", "all"])
    return response


##############################
#  magento api proxy         #
##############################


class MagentoAPI(magento.api.API):

    magento_method = u""

    def __init__(self, request):
        settings = request.registry.settings
        apiurl = settings["magento_apiurl"]
        rpc_user = settings["magento_rpc_user"]
        rpc_secret = settings["magento_rpc_secret"]
        super(MagentoAPI, self).__init__(apiurl, rpc_user, rpc_secret)
        self.request = request

    def single_call(self, resource_path, arguments=[]):
        """Send magento api v.1 call"""
        return self.call(resource_path, arguments)

    def multi_call(self, calls):
        """Send magento api v.1 multiCall"""
        # slice calls to make magento happy and send
        results = []
        for i in range(0, len(calls), 100):
            calls_chunk = calls[i:i + 100]
            results_chunk = self.multiCall(calls_chunk)
            results += results_chunk
        # raise error if something went wrong
        errors = []
        success = []
        for x in results:
            if isinstance(x, dict) and "faultCode" in x:
                errors.append(x)
            else:
                success.append(x)
        if errors:
            raise exceptions.WebshopAPIErrors(errors, success)
        # return results
        return success


######################################
# magento catalog api proxy helpers  #
######################################


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


def get_tier_price_data(appstruct):
    return appstruct.get("tierprices", None)


def get_stock_data(appstruct):
    stock_data = {}
    status = appstruct.get("inventory_status", None)
    if status:
        stock_data["is_in_stock"] = 1 if status in [2, 7, 8] else 0
    inventory_qty = appstruct.get("inventory_qty", None)
    if inventory_qty:
        stock_data['qty'] = inventory_qty
    min_sale_qty = appstruct.get("min_sale_qty", None)
    if min_sale_qty:
        stock_data["use_config_min_sale_qty"] = 0
        stock_data["min_sale_qty"] = min_sale_qty
    max_sale_qty = appstruct.get("max_sale_qty", None)
    if max_sale_qty:
        stock_data["use_config_max_sale_qty"] = 0
        stock_data["max_sale_qty"] = max_sale_qty
    increment = appstruct.get("inventory_qty_increments", None)
    if increment:
        stock_data['use_config_enable_qty_inc'] = 0
        stock_data['use_config_qty_increments'] = 0
        stock_data['enable_qty_increments'] = 1
        stock_data['qty_increments'] = increment
    backorder = appstruct.get("backorders_allow", None)
    if backorder is True:
        stock_data["use_config_backorders"] = 0
        stock_data["backorders"] = 2
        stock_data["min_qty"] = -10000000
    if backorder is False:
        stock_data["use_config_backorders"] = 0
        stock_data["backorders"] = 0
        stock_data["min_qty"] = 0
    return stock_data or None


##############################
#  magento catalog api proxy #
##############################


class MagentoCatalogAPI(MagentoAPI):

    entity_data_key = u""
    magento_type = u""
    magento_method = u""

    items = None
    item_groups = None
    categories = None
    entities = None

    def __init__(self, request):
        super(MagentoCatalogAPI, self).__init__(request)
        self.request = request
        self.items = request.root.app_root["items"]
        self.categories = request.root.app_root["categories"]
        self.item_groups = request.root.app_root["item_groups"]
        self.entities = getattr(self, self.entity_data_key, [])

    def delete(self, webshop_ids):
        for webshop_id in webshop_ids:
            try:
                self.single_call(self.magento_method + "delete", [webshop_id])
            except Fault as e:  # TODO catch only not exists errors
                if e.faultCode == "101":  # we ignore "does not exists" errors
                    pass
        return webshop_ids

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

    def list(self):
        """to be implemented in subclass"""
        pass

    def update(self, appstructs):
        calls = []
        webshop_ids = []
        for appstruct in appstructs:
            entity_id = appstruct["id"]
            webshop_id = self.entities[entity_id].webshop_id
            webshop_ids.append(webshop_id)
            calls.append(
                [self.magento_method + 'update',
                 [webshop_id,
                  self._to_update_data(appstruct),
                  ]
                 ])
        self.multi_call(calls)
        return webshop_ids

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
            else:
                calls.append([self.magento_method + "update",
                              [webshop_id, {"is_anchor": 1}]])
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


class Items(MagentoCatalogAPI):

    entity_data_key = u"items"
    magento_type = u"simple"
    magento_method = u"catalog_product."

    def delete_all(self):
        results = self.single_call(self.magento_method + "list",
                                   [{'type': {'ilike': self.magento_type}}])
        webshop_ids = [x["product_id"] for x in results]
        self.delete(webshop_ids)

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
            ("tax_class_id", appstruct.get("tax_class", None)),
            ("tier_price", get_tier_price_data(appstruct)),
            ("stock_data", get_stock_data(appstruct))]
        data.update(dict([x for x in extradata_tuples if x[1] is not None]))
        additional = {}
        if "__type__" in appstruct:
            additional["webshopapi_type"] = appstruct["__type__"]
        if "id" in appstruct:
            additional["webshopapi_id"] = appstruct["id"]
        if additional:
            data["additional_attributes"] = {"single_data": additional}
        return data

    def _to_update_shops_data(self, appstruct, lang, country="default"):
        """transforms item appstruct to magento update appstruct dictionary.
           returns only StringTranslation values
        """

        name = get_translation(appstruct, "title", lang)
        url_key = utils.get_url_slug(appstruct, lang) if name else None
        data_tuples = [
            ("name", name),
            ("url_key", url_key),
            ("description", get_translation(appstruct, "description", lang)),
            ("short_description", get_translation(appstruct,
                                                  "short_description", lang)),
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


class Categories(MagentoCatalogAPI):

    entity_data_key = u"categories"
    magento_type = u"category"
    magento_method = u"catalog_category."

    def delete_all(self):
        webshop_ids = [x["category_id"] for x in self.list() if
                       x["category_id"] > 2]
        self.delete(webshop_ids)

    def list(self):
        results = self.single_call(self.magento_method + "tree")

        def children(category, res):
            category["category_id"] = int(category["category_id"])
            res.append(category)
            for child in category["children"]:
                children(child, res)
            return res
        return children(results, [])

    def update_shops(self, webshop_ids, appstructs):
        calls = []
        for webshop_id, appstruct in zip(webshop_ids, appstructs):
            storeviews = get_storeviews(appstruct)
            for storeviewname, enabled, lang, country in storeviews:
                data = self._to_update_shops_data(appstruct, lang, country)
                if enabled:
                    data["is_active"] = 1
                else:
                    data["is_active"] = 0
                if data:
                    calls.append([self.magento_method + 'update',
                                  [webshop_id, data, storeviewname]])
        return self.multi_call(calls)

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
        additional = {}
        if "__type__" in appstruct:
            additional["webshopapi_type"] = appstruct["__type__"]
        if "id" in appstruct:
            additional["webshopapi_id"] = appstruct["id"]
        if additional:
            data["additional_attributes"] = {"single_data": additional}
        return data

    def _to_update_shops_data(self, appstruct, lang, country="default"):
        """transforms item appstruct to magento update appstruct dictionary.
           returns only StringTranslation values
        """
        name = get_translation(appstruct, "title", lang)
        url_key = utils.get_url_slug(appstruct, lang) if name else None
        data_tuples = [("name", name),
                       ("url_key", url_key),
                       ("short_description",
                        get_translation(appstruct, "short_description", lang)),
                       ]
        return dict([x for x in data_tuples if x[1] is not None])


###############################
#  magento sales api helpers  #
###############################


def order_data_to_appstruct(data):
    schema = schemata.Order()
    data.update(data["payment"])
    data["website"] = data["store_name"].splitlines()[0]
    data["shop"] = data["store_name"].splitlines()[1]
    data["customer_is_guest"] = bool(int(data["customer_is_guest"]))
    data["order_increment_id"] = int(data["increment_id"])
    for item in data["items"]:
        item["title"] = item["name"]
        item["free_shipping"] = bool(int(item["free_shipping"]))
        item["order_item_id"] = item["item_id"]
    order = schema.deserialize(data)
    return order


######################
#  magento sales api #
######################


class MagentoSalesAPI(MagentoAPI):

    magento_method = u""
    colander_schema = None


    def list(self):
        """to be implemented in subclass"""
        pass

    def order_add_comment(self, appstructs):
        calls = []
        for appstruct in appstructs:
            order_id = appstruct["order_increment_id"]
            status = appstruct["status"]
            comment= appstruct.get("comment", u"")
            email = int(appstruct.get("notify", False))
            include_comment = 1
            calls.append(['sales_order.addComment',
                          [order_id, status, comment, email, include_comment]])
        return [bool(x) for x in self.multi_call(calls)]

    def order_can_capture(self, order_id):
        can_capture = False
        order_data = self.single_call("sales_order.info", [order_id])
        tx_status = order_data.get('payone_transaction_status', '')
        if "APPROVED" in tx_status:
            can_capture = True
        return can_capture


class SalesOrders(MagentoSalesAPI):

    def list(self, status="pending"):
        orders = []
        filters = {"status": status}
        orders_data = self.single_call("sales_order.list", [filters])
        for order_data in orders_data:
            increment_id = order_data["increment_id"]
            order_data = self.single_call("sales_order.info", [increment_id])
            order = order_data_to_appstruct(order_data)
            orders.append(order)
        return orders



class SalesInvoices(MagentoSalesAPI):

    magento_method = u"sales_order_invoice."

    def create(self, appstructs):
        calls = []
        for appstruct in appstructs:
            # create invoice
            calls.append([self.magento_method + 'create',
                          self._create_arguments(appstruct)])
        invoice_ids = [int(x) for x in self.multi_call(calls)]
        return invoice_ids

    def _create_arguments(self, appstruct):
        order_increment_id = appstruct["order_increment_id"]
        comment = appstruct["comment"]
        email = int(appstruct["notify"])
        include_comment = 1
        items_qty = {}
        for i in appstruct["order_item_qtys"]:
            order_item_id = str(i["order_item_id"])
            qty = float(i["qty"])
            items_qty[order_item_id] = qty
        return [order_increment_id, items_qty, comment, email, include_comment]


    def capture(self, invoice_id):
        return bool(self.single_call(self.magento_method + "capture",
                                     [invoice_id]))



# TODO docu inventory status

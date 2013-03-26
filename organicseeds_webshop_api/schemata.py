# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
from decimal import Decimal as PyDec
import json
from colander import (
    MappingSchema,
    SequenceSchema,
    SchemaNode,
    String,
    Float,
    Decimal,
    Bool,
    Integer,
    OneOf,
    Range,
    Regex,
    deferred
)


##############
# Attributes #
##############

validate_identifier = Regex(u'^[a-zA-Z0-9_]+$')

validate_gt_eq_null = Range(min=1)

validate_gt_null =  Range(min=0)

validate_website = validator=OneOf(["ch_website",
                                    "de_website",
                                    "fr_website",
                                    "it_website"
                                   ])

validate_customer_group = OneOf([0,1,2,3])


class Shops(MappingSchema):
    de_hobby = SchemaNode(Bool(), missing=False, default=False, required=False)
    de_profi = SchemaNode(Bool(), missing=False, default=False, required=False)
    de_resell = SchemaNode(Bool(), missing=False, default=False, required=False)
    ch_hobby = SchemaNode(Bool(), missing=False, default=False, required=False)
    ch_profi = SchemaNode(Bool(), missing=False, default=False, required=False)
    ch_resell = SchemaNode(Bool(), missing=False, default=False, required=False)
    fr_hobby = SchemaNode(Bool(), missing=False, default=False, required=False)
    fr_profi = SchemaNode(Bool(), missing=False, default=False, required=False)
    fr_resell = SchemaNode(Bool(), missing=False, default=False, required=False)


class StringTranslation(MappingSchema):
    default = SchemaNode(String())
    de = SchemaNode(String(), missing="", default="", required=False)
    fr = SchemaNode(String(), missing="", default="", required=False)
    it = SchemaNode(String(), missing="", default="", required=False)
    en = SchemaNode(String(), missing="", default="", required=False)
    #TODO test missing/defaults/require
    #TODO support generic websites/shops


class IDTitle(MappingSchema):

    id = SchemaNode(String(), validator=validate_identifier)
    title = StringTranslation()


class DecimalWebsites(MappingSchema):
    default = SchemaNode(Decimal())
    ch_website = SchemaNode(Decimal(), default=PyDec(), missing=PyDec(), required=False)
    de_website = SchemaNode(Decimal(), default=PyDec(), missing=PyDec(), required=False)
    fr_website = SchemaNode(Decimal(), default=PyDec(), missing=PyDec(), required=False)
    it_website = SchemaNode(Decimal(), default=PyDec(), missing=PyDec(), required=False)


class TierPrice(MappingSchema):
    website = SchemaNode(String(), validate=validate_website)
    customer_group = SchemaNode(Integer(), validator=validate_customer_group)
    min_sale_qty = SchemaNode(Integer())
    price = SchemaNode(Decimal())


class TierPrices(SequenceSchema):
    tierprice = TierPrice()


##############
# Categories #
##############


class Category(MappingSchema):
    foo = SchemaNode(String())
    bar = SchemaNode(String())
    baz = SchemaNode(String(), required=False)


class Categories(SequenceSchema):
    category = Category()

class CategoriesList(MappingSchema):
    categories = Categories()


##############################################
# ItemGroups (shop configuratable products)  #
##############################################


#########################
# Items (shop products) #
#########################

# read test/testdata/items_post.py for example data

@deferred
def deferred_validate_unit_of_measure_id(node, kw):
    request = kw["request"]
    data = json.loads(request.body)
    measures = data.get('unit_of_measures')
    measure_ids = [x["id"] for x in measures]
    return OneOf(measure_ids)


@deferred
def deferred_validate_vpe_type_id(node, kw):
    request = kw["request"]
    data = json.loads(request.body)
    measures = data.get('vpe_types')
    measure_ids = [x["id"] for x in measures]
    return OneOf(measure_ids)


class UnitOfMeasure(MappingSchema):
    id = SchemaNode(String())
    title = StringTranslation()


class UnitOfMeasures():
    unit_of_measure = UnitOfMeasure()

class VPEType(MappingSchema):
    id = SchemaNode(String())
    title = StringTranslation()
    legend = StringTranslation()


class VPETypes(SequenceSchema):
    vpe_type = VPEType()

class Item(MappingSchema):
    id = SchemaNode(String())  # TODO validate IDs
    parent_id = SchemaNode(String()) # TODO validate
    __type__ = SchemaNode(String(), validator=OneOf(["sortendetail_vpe",
                                                     "default_vpe"]))
    shops = Shops
    title = StringTranslation()
    sku = SchemaNode(String())
    group = SchemaNode(String(), validator=OneOf(["saatgut",
                                                  "pflanzgut",
                                                  "sonstiges"]))
    vpe_default = SchemaNode(Bool())
    vpe_type_id = SchemaNode(String(), validator=
                             deferred_validate_vpe_type_id)
    weight_brutto = SchemaNode(Float())
    weight_netto = SchemaNode(Float())
    unit_of_measure_id = SchemaNode(String(), validator=\
                                    deferred_validate_unit_of_measure_id)
    price = DecimalWebsites()
    tierprices = TierPrices()
    tax_class = SchemaNode(Integer(), validator=OneOf([0,
                                                       2,
                                                       4,
                                                       5]))
    quality_id = SchemaNode(String())
    min_sale_qty = SchemaNode(Integer(), default=1, missing=1, required=False) # TODO not <= 0 validation
    max_sale_qty = SchemaNode(Integer(), default=1000000, missing=1000000, required=False)
    inventory_status = SchemaNode(Integer(), validator=OneOf([1,2,3,4,5,6,7,8]))


class Items(SequenceSchema):
    item = Item()


class ItemsList(MappingSchema):
    """Test"""
    unit_of_measures = UnitOfMeasures()
    vpe_types = VPETypes()
    items =  Items()




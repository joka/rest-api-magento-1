# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
import json
from colander import (
    MappingSchema,
    SequenceSchema,
    TupleSchema,
    SchemaNode,
    String,
    Float,
    Decimal,
    Bool,
    Integer,
    OneOf,
    Range,
    Regex,
    deferred,
    url
)


##############
# Attributes #
##############

class URL(SchemaNode):

    schema_type = String
    validator = url


class RelativeFilePathUnix(SchemaNode):

    schema_type = String
    validator=Regex(u'^[a-zA-Z0-9\_\-\.][a-zA-Z0-9_\-/\.]+$')


class IntegerGtEqNull(SchemaNode):

    schema_type = Integer
    validator = Range(min=0)


class IntegerGtNull(SchemaNode):

    schema_type = Integer
    validator = Range(min=1)

class Identifier(SchemaNode):

    schema_type = String
    validator=Regex(u'^[a-zA-Z0-9_]+$')


class ShopID(SchemaNode):

    schema_type = String
    validator = OneOf(["ch_hobby",
                       "ch_profi",
                       "ch_resell",
                       "de_hobby",
                       "de_profi",
                       "de_resell",
                       "fr_hobby",
                       "fr_profi",
                       "fr_resell",
                       ])

class WebsiteID(SchemaNode):

    schema_type = String
    validator=OneOf(["ch_website",
                     "de_website",
                     "fr_website",
                    ])



validate_customer_group = OneOf([0,1,2,3])


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
    vpe_types = data.get('vpe_types')
    vpe_type_ids = [x["id"] for x in vpe_types]
    return OneOf(vpe_type_ids)




class StringTranslation(MappingSchema):
    default = SchemaNode(String(), missing=u"", default=u"", required=False )
    de = SchemaNode(String(), missing=u"", default=u"", required=False)
    fr = SchemaNode(String(), missing=u"", default=u"", required=False)
    it = SchemaNode(String(), missing=u"", default=u"", required=False)
    en = SchemaNode(String(), missing=u"", default=u"", required=False)


class IDList(SequenceSchema):

    id = Identifier()


class TextLink(MappingSchema):

    id = Identifier()
    text = StringTranslation()
    url = URL(default=u"", missing=u"", required=False)


class TextLinks(SequenceSchema):

    textlink = TextLink()


class Measure(MappingSchema):

    count = SchemaNode(Float())
    unit = SchemaNode(String())


class Weekmatrix(TupleSchema):

    kw1 = SchemaNode(Bool())
    #kw7, kw8, kw9, kw10, kw11, kw12 = SchemaNode(Bool())
    #kw13, kw14, kw15, kw16, kw17, kw18 = SchemaNode(Bool())
    #kw19, kw20, kw21, kw22, kw23, kw24 = SchemaNode(Bool())
    #kw25, kw26, kw27, kw28, kw29, kw30 = SchemaNode(Bool())
    #kw31, kw32, kw33, kw34, kw35, kw36 = SchemaNode(Bool())
    #kw37, kw38, kw39, kw40, kw41, kw42 = SchemaNode(Bool())
    #kw43, kw44, kw45, kw46, kw47, kw48 = SchemaNode(Bool())


class BaseAttribute(MappingSchema):

    id = Identifier()
    title = StringTranslation()
    order = IntegerGtNull()
    group = Identifier()
    value = SchemaNode(String())


class TextAttribute(BaseAttribute):

    value = TextLinks


class TextAttributes(SequenceSchema):

    textattribute = TextAttribute()


class MeasureAttribute(BaseAttribute):

    value = Measure()


class MeasureAttributes(SequenceSchema):

    measureattribute = MeasureAttribute()


class BoolAttribute(BaseAttribute):

    value = SchemaNode(Bool())


class BoolAttributes(SequenceSchema):

    boolattribute = BoolAttribute()


class WeekmatrixAttribute(BaseAttribute):

    value = Weekmatrix

class WeekmatrixAttributes(SequenceSchema):

    weekmatrixattribute = WeekmatrixAttribute()


class FileAttribute(BaseAttribute):

    value = RelativeFilePathUnix()


class FileAttributes(SequenceSchema):

    fileattribute = FileAttribute()


class LinkAttribute(BaseAttribute):

    value = URL()


class LinkAttributes(SequenceSchema):

    textattribute = LinkAttribute()


class Shop(TupleSchema):
    shopeid = ShopID()
    activated = SchemaNode(Bool(), default=False, missing=False)


class Shops(SequenceSchema):
    shop = Shop()            # TODO test empty list


class WebsitePrice(TupleSchema):

    websiteid = WebsiteID()
    price = SchemaNode(Decimal())


class WebsitePrices(SequenceSchema):

    websiteprice = WebsitePrice()


class Price(MappingSchema):
    default = SchemaNode(Decimal())
    websites = WebsitePrices()


class TierPrice(MappingSchema):
    website = WebsiteID()
    customer_group = SchemaNode(Integer(), validator=validate_customer_group)
    min_sale_qty = SchemaNode(Integer())
    price = SchemaNode(Decimal())


class TierPrices(SequenceSchema):
    tierprice = TierPrice()


#########################
# ItemNode (Base class) #
#########################


class BasicNode(MappingSchema):

    id = Identifier()
    __type__ = SchemaNode(String())
    parent_id = Identifier(default=None, missing=None)
    order = IntegerGtNull()
    shops = Shops()
    title = StringTranslation()
    shortdescription = StringTranslation()


##############
# Categories #
##############

class Synonym(MappingSchema):

    id = Identifier()
    title = SchemaNode(String())


class Synonyms(SequenceSchema):

    synonym=Synonym()


class SynonymTranslations(MappingSchema):

    de_de = Synonyms(default=[], missing=[], required=False)
    it_it = Synonyms(default=[], missing=[], required=False)
    fr_fr = Synonyms(default=[], missing=[], required=False)
    de_ch = Synonyms(default=[], missing=[], required=False)
    it_ch = Synonyms(default=[], missing=[], required=False)
    fr_ch = Synonyms(default=[], missing=[], required=False)


class Category(BasicNode):

    __type__ = SchemaNode(String(), validator=OneOf(["sortenuebersicht",
                                                     "category"]))
    synonyms = SynonymTranslations(default={}, missing={}, required=False)
    text_attributes = TextAttributes(default=[], missing=[], required=False)
    measure_attributes = MeasureAttributes(default=[], missing=[], required=False)
    bool_attributes = BoolAttributes(default=[], missing=[], required=False)
    weekmatrix_attributes = WeekmatrixAttributes(default=[], missing=[], required=False)
    file_attributes = FileAttributes(default=[], missing=[], required=False)
    link_attributes = LinkAttributes(default=[], missing=[], required=False)



class Categories(SequenceSchema):

    category = Category()


class CategoriesList(MappingSchema):

    categories = Categories()


##############################################
# ItemGroups (shop configuratable products)  #
##############################################


class Quality(MappingSchema):

    id = Identifier()
    title = StringTranslation()
    size = SchemaNode(String(), default=u"", missing=u"", required=False)
    tkg = SchemaNode(Float())


class Qualtities(SequenceSchema):

    quality = Quality()


class ItemGroup(Category):

    __type__ = SchemaNode(String(), validator=OneOf(["sortendetail"]))

    category_ids = IDList(default=[], missing=[], required=False)
    description = StringTranslation()

    certificates = IDList(default=[], missing=[], required=False)
    qualities = Qualtities(default=[], missing=[], required=False)


class ItemGroups(SequenceSchema):

    itemgroup = ItemGroup()


class ItemGroupsList(MappingSchema):

    item_groups = ItemGroups()


#########################
# Items (shop products) #
#########################


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


class Item(BasicNode):

    __type__ = SchemaNode(String(), validator=OneOf(["sortendetail_vpe",
                                                     "default_vpe"]))

    category_ids = IDList(default=[], missing=[], required=False)
    description = StringTranslation()

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
    price = Price()
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




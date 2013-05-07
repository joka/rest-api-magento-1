# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4:
import colander
from colander import (
    OneOf,
    Range,
    Regex,
    url
)


##############
# Attributes #
##############


class String(colander.SchemaNode):
    """String, utf-8 encoding
    """

    schema_type = colander.String


class Float(colander.SchemaNode):
    """Float
    """

    schema_type = colander.Float


class Integer(colander.SchemaNode):
    """Integer
    """

    schema_type = colander.Integer


class Decimal(colander.SchemaNode):
    """Decimal
    """

    schema_type = colander.Decimal


class Bool(colander.SchemaNode):
    """Bool

       values: True | False
    """

    schema_type = colander.Bool


class URL(colander.SchemaNode):
    """URL String, utf-8 encoding

       Example value: http://x.org
    """

    schema_type = colander.String
    validator = url


class RelativeFilePathUnix(colander.SchemaNode):
    """Relative path string, utf-8 encoding

       Example values:

         - folder1/file
         - ./folder1/file
         - file
    """

    schema_type = colander.String
    validator = Regex(u'^[a-zA-Z0-9\_\-\.][a-zA-Z0-9_\-/\.]+$')


class IntegerGtEqNull(colander.SchemaNode):
    """Integer greater/equal 0"""

    schema_type = colander.Integer
    validator = Range(min=0)


class IntegerGtNull(colander.SchemaNode):
    """Integer greater 0"""

    schema_type = colander.Integer
    validator = Range(min=1)


class Identifier(colander.SchemaNode):
    """Alpha/numeric/_  String, encoding utf-8

       A global unique identifier.

       Example value: bluABC_123
    """
    schema_type = colander.String
    validator = Regex(u'^[a-zA-Z0-9_]+$')
    title = u"dd"


class Identifiers(colander.SequenceSchema):

    identifier = Identifier()


class ShopID(colander.SchemaNode):
    """Shop Identifier

       Values: ch_hobby | che_profi | ch_resell, fr_hobby | ...
    """

    schema_type = colander.String
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


class WebsiteID(colander.SchemaNode):
    """Website Identifier

       Values: ch_website | de_website | fr_website | ...
    """

    schema_type = colander.String
    validator = OneOf(["ch_website",
                       "de_website",
                       "fr_website",
                       ])


class CustomerGroup(colander.SchemaNode):
    """Customer group id, Integer

       values:
         - 0 = Not logged in
         - 1 = General
         - 2 = Wholesale
         - 3 = Retailer
    """

    schema_type = colander.Integer
    validator = OneOf([0, 1, 2, 3])


class TaxClass(colander.SchemaNode):
    """Item tax class, Integer

       values:

         - 0 = magento default tax group
         - 2 = Taxable goods
         - 4 = (Shipping) 
         - 5 = Reduces Taxable goods
    """
    schema_type = colander.Integer
    validator = OneOf([0, 2, 4, 5])


class ItemTypeGroup(colander.SchemaNode):
    """Item Type Group

       Values: saatgut | pflanzgut | sonstiges
    """
    schema_type = colander.String
    validator = OneOf(["saatgut",
                       "pflanzgut",
                       "sonstiges"])


class InventoryStatus(colander.SchemaNode):
    """Iventory status, Integer

       values: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
    """
    schema_type = colander.Integer
    validator = OneOf([1, 2, 3, 4, 5, 6, 7, 8])


class StringTranslation(colander.MappingSchema):
    """Translated String

       value:

         default : String   # optional

         de : String        # optional

         fr : String        # optional

         it : String        # optional

         en : String        # optional
    """

    default = String(missing=u"", default=u"", required=False)
    de = String(missing=u"", default=u"", required=False)
    fr = String(missing=u"", default=u"", required=False)
    it = String(missing=u"", default=u"", required=False)
    en = String(missing=u"", default=u"", required=False)


class IDList(colander.SequenceSchema):
    """List of Identifiers

       example value:

       [blue1, blue2, gren1, gren2]
    """

    id = Identifier()


class TextLink(colander.MappingSchema):
    """Text String with optional URL

       value:

         id : Identifier

         text : StringTranslation

         url : URL # optional
    """

    id = Identifier()
    text = StringTranslation()
    url = URL(default=u"", missing=u"", required=False)


class TextLinks(colander.SequenceSchema):
    """List of TextLink"""

    textlink = TextLink()


class Measure(colander.MappingSchema):
    """Measurement

       value:

          count: Float  # for example 1.0

          unit : String # for example "mm"
    """

    count = Float()
    unit = String()


class Weekmatrix(colander.TupleSchema):
    """Enable or Disable the 48 Weeks of the year

       value: [Bool, Bool, Bool, ...]
    """

    kw1 = Bool()
    kw2 = Bool()
    kw3 = Bool()
    kw4 = Bool()
    kw5 = Bool()
    kw6 = Bool()
    kw7 = Bool()
    kw8 = Bool()
    kw9 = Bool()
    kw10 = Bool()
    kw11 = Bool()
    kw12 = Bool()
    kw13 = Bool()
    kw14 = Bool()
    kw15 = Bool()
    kw16 = Bool()
    kw17 = Bool()
    kw18 = Bool()
    kw19 = Bool()
    kw20 = Bool()
    kw21 = Bool()
    kw22 = Bool()
    kw23 = Bool()
    kw24 = Bool()
    kw25 = Bool()
    kw26 = Bool()
    kw27 = Bool()
    kw28 = Bool()
    kw29 = Bool()
    kw30 = Bool()
    kw31 = Bool()
    kw32 = Bool()
    kw33 = Bool()
    kw34 = Bool()
    kw35 = Bool()
    kw36 = Bool()
    kw37 = Bool()
    kw38 = Bool()
    kw39 = Bool()
    kw40 = Bool()
    kw41 = Bool()
    kw42 = Bool()
    kw43 = Bool()
    kw44 = Bool()
    kw45 = Bool()
    kw46 = Bool()
    kw47 = Bool()
    kw48 = Bool()


class BaseAttribute(colander.MappingSchema):
    """Attribute

       value:

         id : Identifier

         title : StringTranslation

         order : IntegerGtNull

         value : String
    """

    id = Identifier()
    title = StringTranslation()
    order = IntegerGtNull()
    group = Identifier()
    value = String()


class TextAttribute(BaseAttribute):
    """Text Strings with optional URL

       value:

         id : Identifier

         title : StringTranslation

         order : IntegerGtNull

         value : sequence of TextLink
    """
    value = TextLinks


class TextAttributes(colander.SequenceSchema):

    textattribute = TextAttribute()


class MeasureAttribute(BaseAttribute):
    """Unit and count to measure

       value:

         id : Identifier

         title : StringTranslation

         order : IntegerGtNull

         value :

            count : Float # example 1.2

            unit : String # example "(mm)"
    """

    value = Measure()


class MeasureAttributes(colander.SequenceSchema):

    measureattribute = MeasureAttribute()


class BoolAttribute(BaseAttribute):
    """Enable or disable a property

       value:

         id : Identifier

         title : StringTranslation

         order : IntegerGtNull

         value : Bool
    """

    value = Bool()


class BoolAttributes(colander.SequenceSchema):

    boolattribute = BoolAttribute()


class WeekmatrixAttribute(BaseAttribute):
    """Enable or Disable weeks of the year.

       value:

         id : Identifier

         title : StringTranslation

         order : IntegerGtNull

         value : [Bool, Bool, ... ] # one Bool for every 48 weeks
    """

    value = Weekmatrix


class WeekmatrixAttributes(colander.SequenceSchema):

    weekmatrixattribute = WeekmatrixAttribute()


class FileAttribute(BaseAttribute):
    """Relative path

       value:

         id: Identifiers

         title : StringTranslation

         order : IntegerGtNull

         value : RelativeFilePathUnix

       Example values:

       - folder1/file
       - ./folder1/file
       - file
    """

    value = RelativeFilePathUnix()


class FileAttributes(colander.SequenceSchema):

    fileattribute = FileAttribute()


class LinkAttribute(BaseAttribute):
    """URL

       value:

         id: Identifiers

         title : StringTranslation

         order : IntegerGtNull

         value : URL

       Example value: http://x.org
    """

    value = URL()


class LinkAttributes(colander.SequenceSchema):

    textattribute = LinkAttribute()


class Shop(colander.TupleSchema):
    """Activate entity in this Shop

       value: [ShopID, Bool]

       Example values: [ch_hobby, True] | [ch_hobby, True] | [ch_hobby, True]
    """

    shopeid = ShopID()
    activated = colander.SchemaNode(colander.Bool(), default=False,
                                    missing=False)


class Shops(colander.SequenceSchema):

    shop = Shop()


class WebsitePrice(colander.TupleSchema):
    """Price of this item

       value:

         websiteid : WebsiteID

         price : Float
    """

    websiteid = WebsiteID()
    price = Float()


class WebsitePrices(colander.SequenceSchema):

    websiteprice = WebsitePrice()


class TierPrice(colander.MappingSchema):
    """ Tier price of this item

        value:

          website : WebsiteID

          customer_group_id : CustomerGroup

          qty : Integer

          price : Float
    """

    website = WebsiteID()
    customer_group_id = CustomerGroup()
    qty = Integer()
    price = Float()


class TierPrices(colander.SequenceSchema):
    tierprice = TierPrice()


#########################
# ItemNode (Base class) #
#########################


class BasicNode(colander.MappingSchema):
    """Webshop Item entity

       value:

           id : Identifier

           __type__ : String

           parent_id : Identifier # reference to category/item_group for items;
                                  # to category for categories;
                                  # to categories for item_groups

           order : IntegerGtNull

           title : StringTranslation

           short_description : StringTranslation
    """

    id = Identifier()
    __type__ = String()
    parent_id = Identifier(default=None, missing=None)
    order = IntegerGtNull()
    shops = Shops()
    title = StringTranslation()
    short_description = StringTranslation()


##############
# Categories #
##############


class Synonym(colander.TupleSchema):

    id = Identifier()
    title = String()


class Synonyms(colander.SequenceSchema):

    synonym = Synonym()


class SynonymsTranslation(colander.MappingSchema):
    """Synonyms for this category

       value:

           de_de : sequence of [id, Title] # optional

           de_ch : sequence of [id, Title] # optional

           fr_fr : sequence of [id, Title] # optional

           fr_ch : sequence of [id, Title] # optional

           it_it : sequence of [id, Title] # optional

           it_ch : sequence of [id, Title] # optional
    """

    de_de = Synonyms(default=[], missing=[], required=False)
    it_it = Synonyms(default=[], missing=[], required=False)
    fr_fr = Synonyms(default=[], missing=[], required=False)
    de_ch = Synonyms(default=[], missing=[], required=False)
    it_ch = Synonyms(default=[], missing=[], required=False)
    fr_ch = Synonyms(default=[], missing=[], required=False)


class Category(BasicNode):
    """Webshop category entity

       value:

           <BasicNode> fields

           __type__ : String # sortenuebersicht" | "category"

           synonyms : sequence of SynonymsTranslation

           text_attributes : sequence of TextAttribute

           measure_attributes : sequence of MeasureAttribute

           bool_attributes : sequence of BoolAttribute

           weekmatrix_attributes : sequence of WeekmatrixAttribute

           file_attributes : sequence of FileAttribute

           link_attributes : sequence of LinkAttribute
    """
    __type__ = String(validator=OneOf(["sortenuebersicht",
                                       "category"]))
    synonyms = SynonymsTranslation(default={}, missing={}, required=False)
    text_attributes = TextAttributes(default=[], missing=[], required=False)
    measure_attributes = MeasureAttributes(default=[], missing=[],
                                           required=False)
    bool_attributes = BoolAttributes(default=[], missing=[], required=False)
    weekmatrix_attributes = WeekmatrixAttributes(default=[], missing=[],
                                                 required=False)
    file_attributes = FileAttributes(default=[], missing=[], required=False)
    link_attributes = LinkAttributes(default=[], missing=[], required=False)


class Categories(colander.SequenceSchema):

    category = Category()


class CategoriesList(colander.MappingSchema):

    categories = Categories()


attributes_with_inheritance = ["text_attributes", "measure_attributes",
                               "bool_attributes", "weekmatrix_attributes",
                               "file_attributes", "link_attributes"]


##############################################
# ItemGroups (shop configuratable products)  #
##############################################


class Quality(colander.MappingSchema):
    """VPE Quality

       value:

         id : Identifier

         title : StringTranslation

         size : String  # optional

         tkg : Float
    """

    id = Identifier()
    title = StringTranslation()
    size = String(default=u"", missing=u"", required=False)
    tkg = Float()


class Qualtities(colander.SequenceSchema):

    quality = Quality()


class ItemGroup(Category):
    """Webshop item group entity

       value:

         <BasicNode> fields

         <Category> fields

         __type__ : String # sortendetail

         category_ids : sequence of IDList

         description : StringTranslation

         certificates : sequence of DList # psr | bioverita ...

         qualities : sequence of Qualtity
    """

    __type__ = String(validator=OneOf(["sortendetail"]))

    category_ids = IDList(default=[], missing=[], required=False)
    description = StringTranslation()

    certificates = IDList(default=[], missing=[], required=False)
    qualities = Qualtities(default=[], missing=[], required=False)


class ItemGroups(colander.SequenceSchema):

    itemgroup = ItemGroup()


class ItemGroupsList(colander.MappingSchema):
    item_groups = ItemGroups()


#########################
# Items (shop products) #
#########################


class UnitOfMeasure(colander.MappingSchema):
    """Webshop Item data UnitOfMeasure

       value:

           id : Identifier

           title : StringTranslation
    """

    id = Identifier()
    title = StringTranslation()


class UnitOfMeasures(colander.SequenceSchema):

    unit_of_measure = UnitOfMeasure()


class UnitOfMeasuresList(colander.MappingSchema):

    unit_of_measures = UnitOfMeasures()


class VPEType(colander.MappingSchema):
    """Webshop Item data UnitOfMeasure

       value:

           id : Identifier

           title : StringTranslation

           legend : StringTranslation
    """

    id = Identifier()
    title = StringTranslation()
    legend = StringTranslation()


class VPETypes(colander.SequenceSchema):

    vpe_type = VPEType()


class VPETypesList(colander.MappingSchema):

    vpe_types = VPETypes()


class Item(BasicNode):
    """Webshop Item entity

       value:

           <BasicNode> fields

           __type__ : String # sortendetail_vpe | default_vpe

           category_ids : sequence of IDList

           description : StringTranslation

           sku : String # == Artikelnummer

           group : String # saatgut | pflanzgut | sonstiges

           vpe_default = Bool  # default vpe of item group

           vpe_type_id = Identifier # reference to vpe_type

           weight_brutto = Float

           weight_netto = Float

           unit_of_measure_id = Identifier # refernce to unit_of_measure

           price = sequence of WebsitePrice

           tierprices = sequence of TierPrice

           tax_class = TaxClass

           quality_id = Identifier # reference to item_group quality

           inventory_status = Integer # 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8

           inventory_qty = Integer

           min_sale_qty = Integer # default 1

           max_sale_qty = Integer # default 1000000

           inventory_qty_increments: IntegerGtNull # default 1,
             == größe Verpackunseinheit

           backorders_allow: Bool # default False,
             erlaube Bestellungen wenn Lagerbestand < 1
    """

    __type__ = String(validator=OneOf(["sortendetail_vpe",
                                       "default_vpe"]))
    category_ids = IDList(default=[], missing=[], required=False)
    description = StringTranslation()
    sku = String()
    group = ItemTypeGroup()
    vpe_default = Bool()
    vpe_type_id = Identifier()
    weight_brutto = Float()
    weight_netto = Float()
    unit_of_measure_id = Identifier()
    price = WebsitePrices()
    tierprices = TierPrices()
    tax_class = TaxClass()
    quality_id = String()
    inventory_status = InventoryStatus()
    inventory_qty = Integer()
    min_sale_qty = IntegerGtNull(default=1, missing=1, required=False)
    max_sale_qty = IntegerGtNull(default=1000000, missing=1000000,
                                 required=False)
    inventory_qty_increments = IntegerGtNull(default=1, missing=1,
                                             required=False)
    backorders_allow = Bool(default=False, missing=False, required=False)


class Items(colander.SequenceSchema):

    item = Item()


class ItemsList(colander.MappingSchema):

    items = Items()


class ItemUpdate(colander.Schema):
    """Webshop update Item entity

       The value fields are similar to the Item fields.
       The sku, __type__, parent_id, and category_ids
       fields are not allowed.
       All other fields exists, but are optional.
    """
    id = Identifier()
    #__type__ = String(mising=u"", required=False)
    #parent_id = Identifier(missing=u"", required=False)
    order = IntegerGtNull(missing=None, required=False)
    shops = Shops(missing=None, required=False)
    title = StringTranslation(missing=None, required=False)
    short_description = StringTranslation(missing=None, required=False)

    #category_ids = IDList(missing=None, required=False)
    description = StringTranslation(missing=None, required=False)

    #sku = String(missing=None, required=False)
    group = ItemTypeGroup(missing=None, required=False)
    vpe_default = Bool(missing=None, required=False)
    vpe_type_id = Identifier(missing=None, required=False)
    weight_brutto = Float(missing=None, required=False)
    weight_netto = Float(missing=None, required=False)
    unit_of_measure_id = Identifier(missing=None, required=False)
    price = WebsitePrices(missing=None, required=False)
    tierprices = TierPrices(missing=None, required=False)
    tax_class = TaxClass(missing=None, required=False)
    quality_id = String(missing=None, required=False)
    inventory_status = InventoryStatus(missing=None, required=False)
    inventory_qty = Integer(missing=None, required=False)
    min_sale_qty = IntegerGtNull(missing=None, required=False)
    max_sale_qty = IntegerGtNull(missing=None, required=False)
    inventory_qty_increments = IntegerGtNull(missing=None, required=False)
    backorders_allow = Bool(missing=None, required=False)


class ItemsUpdate(colander.SequenceSchema):

    item_update = ItemUpdate()


class ItemsUpdateList(colander.MappingSchema):

    items = ItemsUpdate()


class ItemGet(colander.MappingSchema):
    """Get Webshop Item entity data

       * lang: "default" | "fr" | "de" | "it" ... # default = "default"

       * id: Identifier # Item id
    """

    lang = Identifier(default="default", missing="default", required=False, location="querystring")
    id = Identifier(location="path")

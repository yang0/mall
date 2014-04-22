#_*_coding:utf-8_*_


from django.db import models
from apps.area.models import City
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey
from apps.common.common import get_file_path
from django.contrib.contenttypes import generic
from apps.pic.models import Pic
from django.contrib.auth.models import User
from apps.common.common import get_file_path




class Brand(models.Model):
    name = models.CharField(u'品牌名称', max_length=15L)

    class Meta:
        db_table = 'brand'
        verbose_name = verbose_name_plural = u'品牌'


    def __unicode__(self):
        return self.name


from apps.eav.eav_models import EavProp
class ProductCategory(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    props = models.ManyToManyField(EavProp, through='ProductCategoryProp')

    class MPTTMeta:
        order_insertion_by = ['name']


    class Meta:
        db_table = 'product_category'
        verbose_name = verbose_name_plural = (u'产品分类')

    def __unicode__(self):
        return self.name


class ProductCategoryProp(models.Model):
    product_category = models.ForeignKey(ProductCategory, verbose_name=u'商品分类')
    eav_prop = models.ForeignKey(EavProp, verbose_name=u'商品属性')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        db_table = 'product_category_prop'
        verbose_name = verbose_name_plural = u'定义商品分类有哪些属性'


class ProductItem(models.Model):
    APPROVE_STATUS_CHOICES = (
        (0, u'出售中'),
        (1, u'仓库中'),
    )
    num = models.IntegerField(u'商品数量')
    price = models.IntegerField(u'价格')
    title = models.CharField(u'标题', max_length=20L, null=True, blank=True)
    description = models.CharField(u'描述', max_length=5000L)
    state = models.ForeignKey(City, verbose_name=u'商品所在省份', related_name="state_productitem_set")
    city = models.ForeignKey(City, verbose_name=u'商品所在城市', related_name="city_productitem_set")
    approve_status = models.IntegerField(u'售卖状态', choices=APPROVE_STATUS_CHOICES)
    product_category = models.ForeignKey(ProductCategory, verbose_name=u'叶子类目id')
    pic = models.ImageField(u'主图', upload_to=get_file_path)
    have_3d = models.BooleanField(u'是否有3D模型')
    brand = models.ForeignKey(Brand, verbose_name=u'关联品牌')
    weight = models.DecimalField(u'商品重量 单位：公斤', max_digits=10, decimal_places=0)
    bulk = models.DecimalField(u'商品体积 单位：立方米', max_digits=10, decimal_places=0)
    sell_point = models.CharField(u'卖点描述', max_length=20L, null=True, blank=True)
    packing_num = models.IntegerField(u'箱数')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    creator = models.ForeignKey(User, editable=False, verbose_name=u'')
    item_rank = models.IntegerField(u'推荐指数')
    sold_num = models.IntegerField(u'销量', null=True, blank=True)
    picList = generic.GenericRelation(Pic)

    class Meta:
        db_table = 'product_item'
        verbose_name = verbose_name_plural = u'商品'


    def __unicode__(self):
        return self.title


from apps.eav.eav_models import EavEnumValue, EavProp, EavEnumGroup

from apps.eav.models import EavValue









class ProductItemProp(models.Model):
    product_item = models.ForeignKey(ProductItem, verbose_name=u'商品')
    eav_prop = models.ForeignKey(EavProp, verbose_name=u'动态属性')
    enum_group = models.ForeignKey(EavEnumGroup, verbose_name=u'如果是销售属性，则该字段不为0')
    create_time = models.DateTimeField(u'', auto_now_add=True)

    class Meta:
        db_table = 'product_item_prop'
        verbose_name = verbose_name_plural = u'定义商品有哪些属性'


    def __unicode__(self):
        return self.name








class ProductSku(models.Model):
    product_item = models.ForeignKey(ProductItem, verbose_name=u'商品')
    price = models.DecimalField(u'价格', max_digits=10, decimal_places=0)
    num = models.IntegerField(u'库存数量')
    sold_num = models.IntegerField(u'已销售数量')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        db_table = 'product_sku'
        verbose_name = verbose_name_plural = u'商品sku'

    def __unicode__(self):
        return "%s sku:%s元" % (self.product_item, self.price)



class ProductSkuValue(models.Model):
    product_sku = models.ForeignKey(ProductSku, verbose_name=u'商品sku')
    eav_value = models.ForeignKey(EavValue, verbose_name=u'销售属性值')
    eav_enum_value = models.ForeignKey(EavEnumValue, verbose_name=u'销售属性枚举值')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        db_table = 'product_sku_value'
        verbose_name = verbose_name_plural = u'商品sku值'





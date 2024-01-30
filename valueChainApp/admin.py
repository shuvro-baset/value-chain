from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'product_group', 'uom', 'qty', 'rate', 'stock_qty', 'stock_rate', 'avg_rate']


@admin.register(ProductIssue)
class ProductIssueAdmin(admin.ModelAdmin):
    list_display = ['creator', 'date', 'description', 'total_qty', 'product', 'status', 'production_cost', 'unit_price']


@admin.register(RawMaterials)
class RawMaterialsAdmin(admin.ModelAdmin):
    list_display = ['creator', 'date', 'description', 'product_issue']


@admin.register(RawMaterialsProduct)
class RawMaterialsProductAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.product_name
    list_display = ['product_name', 'uom', 'qty', 'raw_materials', 'product_issue']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['raw_materials', 'creator', 'date', 'description', 'product_issue', 'total_qty', 'total']


@admin.register(PurchaseRecipt)
class PurchaseReciptAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'creator', 'date', 'description', 'product_issue', 'total_qty', 'total']


# @admin.register(CostType)
# class CostTypeAdmin(admin.ModelAdmin):
#     list_display = ['name', 'total']


@admin.register(ProductionCost)
class ProductionCostAdmin(admin.ModelAdmin):
    list_display = ['creator', 'date', 'cost_type', 'product_issue', 'total']


# @admin.register(OthersCost)
# class OthersCostAdmin(admin.ModelAdmin):
#     list_display = ['creator', 'date', 'cost_type', 'product_issue', 'total']


@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ['creator', 'date', 'product_issue', 'total_qty', 'total']


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['creator', 'date', 'description', 'total_qty', 'total']


@admin.register(DeliveryChallan)
class DeliveryChallanAdmin(admin.ModelAdmin):
    list_display = ['sales_order', 'creator', 'date', 'description', 'total_qty', 'total']

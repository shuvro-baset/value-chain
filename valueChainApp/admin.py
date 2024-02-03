from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_group', 'uom', 'qty', 'rate', 'stock_qty', 'stock_rate', 'avg_rate', 'is_finished_good']


@admin.register(ProductIssue)
class ProductIssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'issue_no', 'date', 'description', 'total_qty', 'product', 'status',
                    'production_cost', 'unit_price']


@admin.register(RawMaterials)
class RawMaterialsAdmin(admin.ModelAdmin):
    list_display = ['id', 'raw_materials_no', 'creator', 'date', 'description', 'product_issue', 'status']


@admin.register(RawMaterialsProduct)
class RawMaterialsProductAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.product_name

    list_display = ['id', 'product_name', 'uom', 'qty', 'raw_materials', 'product_issue']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_order_no', 'raw_materials', 'creator', 'date', 'description', 'product_issue',
                    'total_qty', 'total', 'status']


@admin.register(PurchaseOrderProduct)
class PurchaseOrderProductAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.product_name

    list_display = ['id', 'product_name', 'uom', 'qty', 'rate', 'raw_materials', 'purchase_order', 'product_issue']


@admin.register(PurchaseReceipt)
class PurchaseReceiptAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_receipt_no', 'purchase_order', 'creator', 'date', 'description', 'product_issue',
                    'total_qty', 'total']


@admin.register(PurchaseReceiptProduct)
class PurchaseReceiptProductAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.product_name

    list_display = ['id', 'purchase_receipt', 'product_name', 'uom', 'qty', 'rate', 'purchase_order', 'raw_materials',
                    'product_issue']


# @admin.register(CostType)
# class CostTypeAdmin(admin.ModelAdmin):
#     list_display = ['name', 'total']


@admin.register(ProductionCost)
class ProductionCostAdmin(admin.ModelAdmin):
    list_display = ['id', 'creator', 'date', 'cost_type', 'product_issue', 'total']


# @admin.register(OthersCost)
# class OthersCostAdmin(admin.ModelAdmin):
#     list_display = ['creator', 'date', 'cost_type', 'product_issue', 'total']


@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    # ToDo: product name
    list_display = ['id', 'stock_entry_no', 'creator', 'date', 'product_issue', 'product', 'uom', 'qty', 'rate',
                    'total']


@admin.register(StockEntryProduct)
class StockEntryProductAdmin(admin.ModelAdmin):
    # ToDo: product name
    list_display = ['id', 'stock_entry', 'product_issue', 'product', 'uom', 'qty', 'rate']


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'sales_order_no', 'creator', 'date', 'description', 'total_qty', 'total', 'status']


@admin.register(SalesOrderProduct)
class SalesOrderProductAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.product_name

    list_display = ['id', 'sales_order', 'product_name', 'uom', 'qty', 'rate']


@admin.register(DeliveryChallan)
class DeliveryChallanAdmin(admin.ModelAdmin):
    list_display = ['id', 'delivery_challan_no', 'sales_order', 'creator', 'date', 'description', 'total_qty', 'total']


@admin.register(DeliveryChallanProduct)
class DeliveryChallanProductAdmin(admin.ModelAdmin):
    def product_name(self, obj):
        return obj.product.product_name

    list_display = ['id', 'delivery_challan', 'sales_order', 'product_name', 'uom', 'qty', 'rate']

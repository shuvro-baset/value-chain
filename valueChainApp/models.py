from django.conf import settings

User = settings.AUTH_USER_MODEL
from django.db import models


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=300, unique=True)
    product_group = models.CharField(max_length=300, default='Finished Group')
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    stock_qty = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    stock_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    avg_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class ProductIssue(models.Model):
    STATUS = (
        ('OPEN', 'OPEN'),
        ('PROCESSING', 'PROCESSING'),
        ('COMPLETE', 'COMPLETE'),
    )
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    total_qty = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True, blank=True, choices=STATUS, default=STATUS[0])
    production_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class RawMaterials(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)


class RawMaterialsProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    raw_materials = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    product_issue = models.CharField(max_length=50)


class PurchaseOrder(models.Model):
    raw_materials = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class PurchaseOrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    raw_materials = models.CharField(max_length=50)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product_issue = models.CharField(max_length=50)


class PurchaseRecipt(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class PurchaseReceiptProduct(models.Model):
    purchase_receipt = models.ForeignKey(PurchaseRecipt, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    raw_materials = models.CharField(max_length=50)
    purchase_order = models.CharField(max_length=50)
    product_issue = models.CharField(max_length=50)


class CostType(models.Model):
    name = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class ProductionCost(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    cost_type = models.ForeignKey(CostType, on_delete=models.CASCADE)
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class OthersCost(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    cost_type = models.ForeignKey(CostType, on_delete=models.CASCADE)
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class StockEntry(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class StockEntryProduct(models.Model):
    stock_entry = models.ForeignKey(StockEntry, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    product_issue = models.CharField(max_length=50)


class SalesOrder(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class SalesOrderProduct(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class DeliveryChallan(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)


class DeliveryChallanProduct(models.Model):
    delivery_challan = models.ForeignKey(DeliveryChallan, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    sales_order = models.CharField(max_length=50)

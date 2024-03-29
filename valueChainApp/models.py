from django.conf import settings

User = settings.AUTH_USER_MODEL
from django.db import models


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=300, unique=True)
    product_group = models.CharField(max_length=300, default='Finished Goods')
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    stock_qty = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    stock_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    avg_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    current_market_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_finished_good = models.BooleanField(default=False)

class ProductIssue(models.Model):
    STATUS = (
        ('OPEN', 'OPEN'),
        ('PROCESSING', 'PROCESSING'),
        ('COMPLETE', 'COMPLETE'),
    )
    issue_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    total_qty = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS, default=STATUS[0])
    production_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.status == 'COMPLETE':
            # Calculate unit_price only if status is 'COMPLETE'
            if self.total_qty and self.total_qty > 0 and self.production_cost > 0:
                self.unit_price = float(self.production_cost) / float(self.total_qty)
            else:
                # Handle division by zero or missing values
                self.unit_price = 0  # Set to default value

        super().save(*args, **kwargs)


class RawMaterials(models.Model):
    STATUS = (
        ('OPEN', 'OPEN'),
        ('PROCESSING', 'PROCESSING'),
        ('COMPLETE', 'COMPLETE'),
    )
    raw_materials_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=STATUS, default=STATUS[0])

    def save(self, *args, **kwargs):
        if self.product_issue:
            self.product_issue.status = 'PROCESSING'
            self.product_issue.save()
        super().save(*args, **kwargs)


class RawMaterialsProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    raw_materials = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    product_issue = models.CharField(max_length=50)


class PurchaseOrder(models.Model):
    STATUS = (
        ('OPEN', 'OPEN'),
        ('PROCESSING', 'PROCESSING'),
        ('COMPLETE', 'COMPLETE'),
    )
    purchase_order_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    raw_materials = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUS, default=STATUS[0])

    def save(self, *args, **kwargs):
        if self.raw_materials:
            self.raw_materials.status = 'PROCESSING'
            self.raw_materials.save()

        super().save(*args, **kwargs)


class PurchaseOrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    raw_materials = models.CharField(max_length=50)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product_issue = models.CharField(max_length=50)


class PurchaseReceipt(models.Model):
    purchase_receipt_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.purchase_order:
            self.purchase_order.status = 'COMPLETE'
            self.purchase_order.save()

        raw_materials = self.purchase_order.raw_materials
        raw_materials.status = 'COMPLETE'
        raw_materials.save()

        product_issue = self.product_issue
        product_issue.production_cost = float(product_issue.production_cost) + float(self.total)
        product_issue.save()

        super().save(*args, **kwargs)


class PurchaseReceiptProduct(models.Model):
    purchase_receipt = models.ForeignKey(PurchaseReceipt, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    raw_materials = models.CharField(max_length=50)
    purchase_order = models.CharField(max_length=50)
    product_issue = models.CharField(max_length=50)


class ProductionCost(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    cost_type = models.CharField(max_length=250, null=True, blank=True)
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        product_issue = self.product_issue
        product_issue.production_cost = float(product_issue.production_cost) + float(self.total)
        product_issue.save()

        super().save(*args, **kwargs)


class StockEntry(models.Model):
    stock_entry_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    product_issue = models.ForeignKey(ProductIssue, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50, null=True, blank=True)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product = self.product
        product.stock_qty = float(product.stock_qty) + float(self.qty)
        product.stock_rate = float(product.stock_rate) + float(self.total)
        product.avg_rate = float(product.stock_rate) / float(product.stock_qty)
        product.save()


class StockEntryProduct(models.Model):
    stock_entry = models.ForeignKey(StockEntry, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    product_issue = models.CharField(max_length=50)


class SalesOrder(models.Model):
    STATUS = (
        ('OPEN', 'OPEN'),
        ('PROCESSING', 'PROCESSING'),
        ('COMPLETE', 'COMPLETE'),
    )
    sales_order_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUS, default=STATUS[0])


class SalesOrderProduct(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)


class DeliveryChallan(models.Model):
    delivery_challan_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    description = models.TextField()
    total_qty = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        sales_order = self.sales_order
        sales_order.status = 'COMPLETE'
        sales_order.save()


class DeliveryChallanProduct(models.Model):
    delivery_challan = models.ForeignKey(DeliveryChallan, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    uom = models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    sales_order = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product = self.product
        product.stock_qty = float(product.stock_qty) - float(self.qty)
        product.stock_rate = float(product.stock_rate) - (float(self.qty) * float(product.avg_rate))
        product.save()

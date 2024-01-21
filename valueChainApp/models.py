from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=300, unique=True)
    product_group = models.CharField(max_length=300, default='Finished Group')
    uom = models.CharField(max_length=50)
    qty = models.DecimalField( max_digits=8, decimal_places=2)
    rate = models.DecimalField( max_digits=8, decimal_places=2)
    stock_qty = models.DecimalField( max_digits=8, decimal_places=2)
    stock_rate = models.DecimalField( max_digits=8, decimal_places=2)
    avg_rate = models.DecimalField( max_digits=8, decimal_places=2)
# Generated by Django 5.0.1 on 2024-02-01 17:26

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('valueChainApp', '0012_purchaseorder_status_rawmaterials_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PurchaseRecipt',
            new_name='PurchaseReceipt',
        ),
    ]

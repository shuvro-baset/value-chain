# Generated by Django 5.0.1 on 2024-02-03 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valueChainApp', '0004_rename_purchas_receipt_no_purchasereceipt_purchase_receipt_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_finished_good',
            field=models.BooleanField(default=False),
        ),
    ]

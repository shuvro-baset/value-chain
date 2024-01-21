# Generated by Django 5.0.1 on 2024-01-21 18:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valueChainApp', '0002_productissue'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CostType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='OthersCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cost_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.costtype')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.productissue')),
            ],
        ),
        migrations.CreateModel(
            name='ProductionCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cost_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.costtype')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.productissue')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('total_qty', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.product')),
                ('product_issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.productissue')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseRecipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('total_qty', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.product')),
                ('product_issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.productissue')),
                ('purchase_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.purchaseorder')),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.product')),
                ('product_issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.productissue')),
            ],
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='raw_materials',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.rawmaterials'),
        ),
        migrations.CreateModel(
            name='SalesOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('total_qty', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.product')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryChallan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('total_qty', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.product')),
                ('sales_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.salesorder')),
            ],
        ),
        migrations.CreateModel(
            name='StockEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('total_qty', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.product')),
                ('product_issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.productissue')),
            ],
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-05 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valueChainApp', '0007_alter_productissue_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_group',
            field=models.CharField(default='Finished Goods', max_length=300),
        ),
    ]
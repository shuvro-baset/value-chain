# Generated by Django 5.0.1 on 2024-01-31 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valueChainApp', '0011_remove_otherscost_cost_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(blank=True, choices=[('OPEN', 'OPEN'), ('PROCESSING', 'PROCESSING'), ('COMPLETE', 'COMPLETE')], default=('OPEN', 'OPEN'), max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='rawmaterials',
            name='status',
            field=models.CharField(blank=True, choices=[('OPEN', 'OPEN'), ('PROCESSING', 'PROCESSING'), ('COMPLETE', 'COMPLETE')], default=('OPEN', 'OPEN'), max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='status',
            field=models.CharField(blank=True, choices=[('OPEN', 'OPEN'), ('PROCESSING', 'PROCESSING'), ('COMPLETE', 'COMPLETE')], default=('OPEN', 'OPEN'), max_length=100, null=True),
        ),
    ]
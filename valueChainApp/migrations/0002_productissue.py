# Generated by Django 5.0.1 on 2024-01-21 18:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valueChainApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('total_qty', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(blank=True, choices=[('OPEN', 'OPEN'), ('PROCESSING', 'PROCESSING'), ('COMPLETE', 'COMPLETE')], default=('OPEN', 'OPEN'), max_length=100, null=True)),
                ('production_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='valueChainApp.product')),
            ],
        ),
    ]

# Generated by Django 4.1.1 on 2022-11-14 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOOSS', '0012_alter_inventory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_detail',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]

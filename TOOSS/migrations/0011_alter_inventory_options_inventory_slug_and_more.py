# Generated by Django 4.1.1 on 2022-11-07 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOOSS', '0010_customer_fname_customer_lname'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventory',
            options={'ordering': ('item_name',)},
        ),
        migrations.AddField(
            model_name='inventory',
            name='slug',
            field=models.SlugField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='item_name',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterIndexTogether(
            name='inventory',
            index_together={('item_id', 'slug')},
        ),
    ]
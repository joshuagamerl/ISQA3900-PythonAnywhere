# Generated by Django 4.1.2 on 2022-10-24 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOOSS', '0004_rename_order_details_order_detail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50)),
                ('Fname', models.CharField(max_length=50)),
                ('Lname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
            ],
        ),
    ]

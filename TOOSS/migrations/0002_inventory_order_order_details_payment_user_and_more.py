# Generated by Django 4.1.1 on 2022-10-05 02:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('TOOSS', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.CharField(max_length=250)),
                ('item_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('item_stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order_Details',
            fields=[
                ('order_details_id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TOOSS.inventory')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TOOSS.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('card_number', models.PositiveBigIntegerField()),
                ('payment_type', models.CharField(max_length=20)),
                ('ccv_code', models.DecimalField(decimal_places=0, max_digits=3)),
                ('expiration_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TOOSS.order_details')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.AddField(
            model_name='payment',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='TOOSS.user'),
        ),
        migrations.AddField(
            model_name='order_details',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='TOOSS.user'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TOOSS.user'),
        ),
    ]

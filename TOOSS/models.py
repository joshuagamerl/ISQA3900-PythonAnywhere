from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Define the mode for the Customer Table


# class User(models.Model):
#    user_name = models.CharField(max_length=50)
#    email = models.EmailField(max_length=100)
#    phone = models.CharField(max_length=20)
#    address = models.CharField(max_length=200)
#    city = models.CharField(max_length=50)
#    state = models.CharField(max_length=2)
#    zipcode = models.CharField(max_length=10)
#
#    def __str__(self):
#        return self.user_name

class Customer(models.Model):
    cust_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zipcode = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.cust_name)


class Inventory(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100, db_index=True)
    item_description = models.CharField(max_length=250)
    item_cost = models.DecimalField(max_digits=6, decimal_places=2)
    item_stock = models.IntegerField()
    image = models.ImageField(upload_to='inventory/%Y/%m/%d', blank=True)
    slug = models.SlugField(max_length=200, db_index=True)

    class Meta:
        ordering = ('item_name',)
        index_together = (('item_id', 'slug'),)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse('TOOSS:inventory_detail', args=[self.item_id, self.slug])


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')

    PAYMENT_TYPES = (
        ('cc', 'Credit Card'),
        ('dc', 'Debit Card'),
        ('cs', 'Cash'),
        ('ch', 'Check'),
        ('bc', 'Bit Coin'),
    )

    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPES, blank=True, default='cc')
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.payment_id) + " " + str(self.user_name)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_create_date = models.DateTimeField(default=timezone.now)
    order_update_date = models.DateTimeField(default=timezone.now)
    order_paid = models.BooleanField(default=False)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order_id)


class Order_Detail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user_name) + " " + str(self.order_id) + " " + str(self.price)



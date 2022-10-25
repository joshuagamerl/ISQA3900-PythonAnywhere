from django.db import models
from django.utils import timezone

# Define the mode for the Customer Table


class User(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.user_name


class Inventory(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    item_description = models.CharField(max_length=250)
    item_cost = models.DecimalField(max_digits=6, decimal_places=2)
    item_stock = models.IntegerField()

    def __str__(self):
        return self.item_name


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    card_number = models.PositiveBigIntegerField()
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20)
    ccv_code = models.DecimalField(max_digits=3, decimal_places=0)
    expiration_date = models.DateField()
    order_detail_id = models.ForeignKey('Order_Detail', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.payment_id) + " " + str(self.user_name)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_create_date = models.DateTimeField(default=timezone.now)
    order_update_date = models.DateTimeField(default=timezone.now)
    order_paid = models.BooleanField(default=False)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order_id) + " " + str(self.user_name) + " " + str(self.order_paid)


class Order_Detail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user_name) + " " + str(self.order_id) + " " + str(self.price)


class Customer(models.Model):
    cust_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return self.cust_name

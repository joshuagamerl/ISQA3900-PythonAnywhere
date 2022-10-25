from django.contrib import admin
from .models import User, Inventory, Payment, Order, Order_Detail, Customer

# Define the admin options for the Customer Table


class UserList(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'phone')
    list_filter = ('user_name', 'email')
    search_fields = ('user_name', )
    ordering = ['user_name']


class InventoryList(admin.ModelAdmin):
    list_display = ('item_name', 'item_description', 'item_cost', 'item_stock')
    list_filter = ('item_name', 'item_description')
    search_fields = ('item_name',)
    ordering = ['item_name']


class PaymentList(admin.ModelAdmin):
    list_display = ('user_name', 'card_number', 'payment_type', 'ccv_code')
    list_filter = ('user_name', 'payment_type')
    search_fields = ('user_name',)
    ordering = ['user_name']


class OrderList(admin.ModelAdmin):
    list_display = ('order_id', 'user_name', 'order_create_date', 'order_paid')
    list_filter = ('order_id', 'user_name', 'order_paid')
    search_fields = ('user_name', 'order_create_date',)
    ordering = ['order_id']


class OrderDetailList(admin.ModelAdmin):
    list_display = ('user_name', 'order_id', 'item_id', 'price', 'quantity')
    list_filter = ('user_name', 'order_id')
    search_fields = ('user_name', 'order_id', 'item_id',)
    ordering = ['user_name']


class CustomerList(admin.ModelAdmin):
    list_display = ('cust_name', 'email', 'phone')
    list_filter = ('cust_name', 'email')
    search_fields = ('cust_name',)
    ordering = ['cust_name']


admin.site.register(Customer, CustomerList)
admin.site.register(User, UserList)
admin.site.register(Inventory, InventoryList)
admin.site.register(Payment, PaymentList)
admin.site.register(Order, OrderList)
admin.site.register(Order_Detail, OrderDetailList)

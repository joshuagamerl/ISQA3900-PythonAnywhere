from django import forms
from .models import Inventory, Customer, Payment
from django.contrib.auth.models import User


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('item_name', 'item_description', 'item_cost', 'item_stock')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('cust_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode')

class PaymentForm(forms.ModelForm):


    class Meta:
        model = Payment
        fields = ('user_name', 'payment_type', 'order_id', 'paid')
        exclude = ['user_name', 'order_id']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

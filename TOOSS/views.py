from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from _decimal import Decimal
from cart.forms import CartAddInventoryForm
from cart.views import Cart
from cart.context_processors import cart
from django.db.models import F
import datetime
import time
from django.views.decorators.http import require_GET


def register(request):
    users = User.objects.all()
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid() and user_form not in users:
            # cust_form = CustomerForm(request.POST)
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # new_cust = cust_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # time.sleep(10)

            Customer.objects.create(cust_name=new_user, fname=new_user.first_name, lname=new_user.last_name
                                    , email=new_user.email)
            return render(request, 'TOOSS/register_done.html', {'new_user': new_user})
        else:
            notCorrect = 'Username is already taken please try again.'
            user_form = UserRegistrationForm()
            return render(request, 'TOOSS/register.html', {'user_form': user_form, 'notCorrect':notCorrect})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'TOOSS/register.html', {'user_form': user_form})


# now = timezone.now()

def home(request):
    cart = Cart(request)
    return render(request, 'TOOSS/home.html', {'TOOSS': home, 'cart': cart})

def inventory_list(request):
    inventory = Inventory.objects.filter()
    cart = Cart(request)
    # print(inventory)

    return render(request, 'TOOSS/inventory_list.html', {'inventorys': inventory, 'cart': cart})

def inventory_detail(request, item_id, slug):
    inventory = get_object_or_404(Inventory,
                                  item_id=item_id,
                                  slug=slug)
    cart_inventory_form = CartAddInventoryForm()
    cart = Cart(request)
    return render(request,
                  'TOOSS/inventory_detail.html',
                  {'inventory': inventory, 'cart_inventory_form': cart_inventory_form, 'cart': cart})

@login_required
def order_list(request, order=None):
    order = Order.objects.filter(user_name=request.user)
    cart = Cart(request)

    return render(request, 'TOOSS/order_list.html', {'orders': order, 'cart': cart})

@login_required
def customer_list(request):
    cart = Cart(request)
    customer = Customer.objects.filter()
    return render(request, 'TOOSS/customer_list.html',
                  {'customers': customer, 'cart': cart})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        # update
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.updated_date = timezone.now()
            customer.save()
            customer = Customer.objects.filter()
            return render(request, 'TOOSS/customer_list.html',
                          {'customers': customer})
    else:
        # edit
        form = CustomerForm(instance=customer)
    return render(request, 'TOOSS/customer_edit.html', {'form': form})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    cart = Cart(request)
    customer2 = Customer.objects.filter()
    return render(request, 'TOOSS/customer_list.html', {'customers': customer2, 'cart': cart})


@login_required
def summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    order = Order_Detail.objects.filter(user_name=pk)
    sum_order_charge = \
        Order_Detail.objects.filter(user_name=pk).aggregate(Sum('price'))
    # if no product or service records exist for the customer,
    # change the ‘None’ returned by the query to 0.00
    sum = sum_order_charge.get("price__sum")
    if sum== None:
        sum_order_charge = {'price__sum': Decimal('0')}
    return render(request, 'TOOSS/summary.html', {'orders': order,
                                                  'customers': customer,
                                                  'sum_order_charge': sum_order_charge})
@login_required
def order_detail(request, pk):
    cart = Cart(request)
    order = get_object_or_404(Order, pk=pk)
    orders = Order_Detail.objects.filter(order_id=pk)
    inventory = Inventory.objects.all()

    sum_order_charge = \
        Order_Detail.objects.filter(order_id=pk).aggregate(total=Sum(F('price') * F('quantity')))['total']

    sum_order_charge = round(sum_order_charge,2)
    # print(sum_order_charge)
    return render(request, 'TOOSS/order_detail.html', {'order': order, 'orders': orders, 'inventory': inventory,
                                                       'cart': cart, 'sum_order_charge': sum_order_charge})


@require_GET
def searchbar(request):
    if 'search' in request.GET:
        context = request.GET['search']
        post = Inventory.objects.filter(item_name__icontains=context)
    else:
        post = Inventory.objects.none()
    return render(request, 'TOOSS/searchbar.html', {'post': post})

def payment_verf(request):
    cart = Cart(request)
    current_user = request.user
    now = datetime.datetime.now()
    if request.method == 'POST':
        order_form = PaymentForm(request.POST)
        if order_form.is_valid():
            new_order = order_form.save(commit=False)
            order = Order.objects.create(user_name=current_user, order_create_date=now, order_update_date=now
                                         , order_paid=new_order.paid)
            new_order.user_name = current_user
            new_order.order_id = order
            new_order.save()
            # print(cart.cart)
            for i in cart.cart.keys():
                iname = Inventory.objects.get(item_id__in=i)
                # print(item)
                # iname = item.values('item_name')
                # print(iname)
                Order_Detail.objects.create(user_name=current_user
                                            , order_id=order
                                            , item_id=iname
                                            , price=cart.cart[i]['item_cost']
                                            , quantity=cart.cart[i]['quantity'])

            cart.clear()
            return render(request, 'TOOSS/payment_verf_done.html', {'new_order': new_order,
                                                                    'current_user': current_user,
                                                                    'order_id': new_order.order_id})
    else:
        order_form = PaymentForm()
        order = Order.objects.last()
        order_id = order.order_id+1
        return render(request, 'TOOSS/payment_verf.html', {'order_form': order_form, 'current_user': current_user,
                                                           'order_id': order_id})

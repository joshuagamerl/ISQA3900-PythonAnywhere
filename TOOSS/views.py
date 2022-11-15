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

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'TOOSS/register_done.html', {'new_user': new_user})
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
    print(inventory)

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
    return render(request, 'TOOSS/customer_list.html')


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
    inventory = Inventory.objects.filter(item_id__in=Order_Detail.objects.filter(order_id=pk).all())

    sum_order_charge = \
        Order_Detail.objects.filter(order_id=pk).aggregate(total=Sum(F('price') * F('quantity')))['total']

    sum_order_charge = round(sum_order_charge,2)
    # print(sum_order_charge)
    return render(request, 'TOOSS/order_detail.html', {'order': order, 'orders': orders, 'inventory': inventory,
                                                       'cart': cart, 'sum_order_charge': sum_order_charge})

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from TOOSS.models import Inventory
from .cart import Cart
from .forms import CartAddInventoryForm


@require_POST
def cart_add(request, inventory_item_id):
    cart = Cart(request)
    inventory = get_object_or_404(Inventory, item_id=inventory_item_id)
    form = CartAddInventoryForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(inventory=inventory,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, inventory_item_id):
    cart = Cart(request)
    inventory = get_object_or_404(Inventory, item_id=inventory_item_id)
    cart.remove(inventory)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddInventoryForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})

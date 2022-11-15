from decimal import Decimal
from django.conf import settings
from TOOSS.models import Inventory


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        inventory_item_ids = self.cart.keys()
        # get the inventory objects and add them to the cart
        inventorys = Inventory.objects.filter(item_id__in=inventory_item_ids)

        cart = self.cart.copy()
        for inventory in inventorys:
            cart[str(inventory.item_id)]['inventory'] = inventory

        for item in self.cart.values():
            item['item_cost'] = Decimal(item['item_cost'])
            item['total_item_cost'] = item['item_cost'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, inventory, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        inventory_item_id = str(inventory.item_id)
        if inventory_item_id not in self.cart:
            self.cart[inventory_item_id] = {'quantity': 0, 'item_cost': str(inventory.item_cost)}
        if update_quantity:
            self.cart[inventory_item_id]['quantity'] = quantity
        else:
            self.cart[inventory_item_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, inventory):
        """
        Remove a product from the cart.
        """
        inventory_item_id = str(inventory.item_id)
        if inventory_item_id in self.cart:
            del self.cart[inventory_item_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['item_cost']) * item['quantity'] for item in self.cart.values())

    def get_total_count(self):
        total_item = 0
        for item in self.cart.values():
            total_item += item['quantity']
        return total_item

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()

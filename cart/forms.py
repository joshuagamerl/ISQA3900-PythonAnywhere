from django import forms


INVENTORY_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddInventoryForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=INVENTORY_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

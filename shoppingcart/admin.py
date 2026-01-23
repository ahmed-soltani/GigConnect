from django.contrib import admin
from shoppingcart.models import ShoppingCart, ShoppingCartItem

# Register your models here.
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
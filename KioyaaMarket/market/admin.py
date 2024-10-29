from django.contrib import admin
from .models import Item, Category, Client, ItemBuy, ShoppingList
# Register your models here.

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(ShoppingList)
admin.site.register(ItemBuy)
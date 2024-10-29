from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='static/img/')
    price = models.FloatField()
    category = models.ManyToManyField(Category)
    stock = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.price}'

class ItemBuy(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def total_price(self) -> float:
        return self.item.price * self.amount
    
    def __str__(self):
        return f'{self.item} {self.amount}'


class ShoppingList(models.Model):
    items = models.ManyToManyField(ItemBuy)

class Client(User):
    ShoppingList = models.OneToOneField(ShoppingList, on_delete=models.CASCADE, null=True, blank=True)
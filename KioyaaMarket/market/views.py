from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Item, Category, Client, ItemBuy, ShoppingList
from django.contrib.auth import authenticate, login as auth_login
from django.utils.http import urlencode
from django.shortcuts import redirect, get_object_or_404
# Create your views here.


def index(request):    
    items = Item.objects.all()
    category = Category.objects.all()
    context = {
        'items': items,
        'category': category,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def category(request, name):
    if not request.user.is_authenticated:
        name = urlencode({'next': f'/category/{name}'})
        return HttpResponseRedirect("/login/?"+ name)
    
    items = Item.objects.filter(category__name = name)
    category = Category.objects.all()
    context = {
        'items': items,
        'category': category,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def cart(request):
    client = Client.objects.get(username = request.user.username)
    shopping_list = client.ShoppingList
    items_buy = shopping_list.items.all()
    items = [item_buy.item for item_buy in items_buy]

    total = 0
    for i in items_buy:
        total += i.total_price()

    context = {
        'client': client,
        'shopping_list' : shopping_list,
        'items_buy' : items_buy,
        'items' : items,
        'total': total,
    }
    template = loader.get_template('cart.html')
    return HttpResponse(template.render(context, request))

def add(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/?")
    if request.method == 'POST':
        user = request.user
        nameItem = request.POST.get('name')
        amount = request.POST.get('amount')

        client = get_object_or_404(Client, username=user.username)
        item = get_object_or_404(Item, name=nameItem)

        if not isinstance(client, Client):
            return redirect(login)
        
        if not client.ShoppingList:
            shopping_list = ShoppingList.objects.create()
            client.ShoppingList = shopping_list
            client.save()
        else:
            shopping_list = client.ShoppingList

        item_buy, created = ItemBuy.objects.get_or_create(item=item)
        item_buy.amount += int(amount)
        item_buy.save()

        shopping_list.items.add(item_buy)
        shopping_list.save()

        return redirect(index)
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def remove(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/?")
    if request.method == 'POST':
        user = request.user
        nameItem = request.POST.get('name')
        amount = request.POST.get('amount')

        client = get_object_or_404(Client, username=user.username)
        item = get_object_or_404(Item, name=nameItem)

        if not isinstance(client, Client):
            return redirect(login)
        
        
        shopping_list = client.ShoppingList

        item_buy = ItemBuy.objects.get(item=item)
        item_buy.amount -= int(amount)
        item_buy.save()

        shopping_list.items.add(item_buy)
        shopping_list.save()

        return redirect(cart)
    template = loader.get_template('cart.html')
    return HttpResponse(template.render())

def pay(request):
    client = Client.objects.get(username = request.user.username)
    shopping_list = client.ShoppingList
    items_buy = shopping_list.items.all()

    for item_buy in items_buy:
        item = item_buy.item
        item.stock -= item_buy.amount
        item.save()
    shopping_list.items.clear()

    return redirect(index)
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(index, permanent=True)
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    template = loader.get_template('login.html')
    context = {
        'next': next
    }
    return HttpResponse(template.render(context, request))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            user = Client.objects.create_user(username=username, password=password)
            user.save()
            return redirect(login)
        else:
            return render(request, 'register.html', {'error': 'Invalid credentials'})
    
    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))
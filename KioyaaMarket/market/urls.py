from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cart/", views.cart, name="cart"),
    path("category/<str:name>/", views.category, name="category"),
    path("add/", views.add, name="add"),
    path("remove/", views.remove, name="remove"),
    path("pay/", views.pay, name="pay"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
]
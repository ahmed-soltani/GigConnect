from django.urls import path
from . import views

urlpatterns = [
    path('show/', views.show_shopping_cart, name='shopping_cart_show'),
    path('pay/', views.pay, name='shopping_cart_pay'),
]
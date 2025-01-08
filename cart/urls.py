from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_list, name='cart_list'),
    path('add/', views.cart_add, name='cart_add'),
    path('update/', views.cart_update, name='cart_update'),
    path('remove/', views.cart_remove, name='cart_remove'),
]


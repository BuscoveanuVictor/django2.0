from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('shop/', views.ShopView, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('', views.index, name='index'),
    path('product/<int:product_id>/', views.productView, name='productView'),
]


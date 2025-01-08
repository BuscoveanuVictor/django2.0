from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from shop.models import Instrument
from .models import Cart
from django.shortcuts import render

def cart_list(request):
    return render(request, 'cart/product_list.html')

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Instrument, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    success, message = cart.add(product, quantity)
    return JsonResponse({
        'success': success,
        'message': message,
        'cart_total': cart.get_total_items(),
        'product_quantity': cart.get_item_quantity(product_id)
    })

def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Instrument, id=product_id)
    quantity = int(request.POST.get('quantity', 0))
    
    success, message = cart.update_quantity(product, quantity)
    return JsonResponse({
        'success': success,
        'message': message,
        'cart_total': cart.get_total_items(),
        'product_quantity': cart.get_item_quantity(product_id)
    })

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Instrument, id=product_id)
    cart.remove(product)
    return JsonResponse({'success': True})
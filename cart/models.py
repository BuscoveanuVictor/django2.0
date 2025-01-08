from decimal import Decimal
from django.conf import settings
from shop.models import Instrument

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        current_quantity = self.cart.get(product_id, {}).get('quantity', 0)
        new_quantity = current_quantity + quantity

        if new_quantity > product.stock:
            return False, "Cantitate insuficientă în stoc!"

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        self.cart[product_id]['quantity'] = new_quantity
        self.save()
        return True, "Produs adăugat cu succes!"

    def update_quantity(self, product, quantity):
        product_id = str(product.id)
        if quantity > product.stock:
            return False, "Cantitate insuficientă în stoc!"
        
        if quantity <= 0:
            if product_id in self.cart:
                del self.cart[product_id]
        else:
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price)
            }
        self.save()
        return True, "Cantitate actualizată!"

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_item_quantity(self, product_id):
        return self.cart.get(str(product_id), {}).get('quantity', 0)

    def save(self):
        self.session.modified = True
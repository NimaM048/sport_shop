from django.utils.functional import SimpleLazyObject

from cart.card_models import Cart
from django.contrib.sessions.models import Session
import datetime


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cart = Cart(request)
        request.cart_item_count = len(cart.cart.values()) if cart.cart else 0
        return self.get_response(request)





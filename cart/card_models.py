from _pydecimal import Decimal

from django.db.models import Sum, F

from home.models import SeriesModel

CARD_SESSION_ID = "cart"


class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(CARD_SESSION_ID)
        if not cart:
            cart = self.session[CARD_SESSION_ID]= {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for items in cart.values():
            product = SeriesModel.objects.get(id=int(items['id']))
            items['product'] = product
            items['unique_id'] = self.unique_id_generator(product.id)

            yield items



    def unique_id_generator(self, id):
        result = f'{id}'
        return result


    def add(self, quantity, product):
        unique = self.unique_id_generator(product.id)
        if unique not in self.cart:
            self.cart[unique] = {'quantity':1, "price": str(product.discount_price), 'id': str(product.id)}

        self.save()

    def remove(self):
        del self.session[CARD_SESSION_ID]

    @property
    def total_price(self):
        total_price = Decimal(0)  # Create an instance of Decimal
        for item in self.cart.values():
            if 'price' in item and item['quantity'] is not None:
                price_str = item['price']
                quantity_str = item['quantity']
                if price_str not in (None, '', 'None'):
                    try:
                        total_price += Decimal(quantity_str) * Decimal(price_str.replace(',', ''))
                    except Exception as e:
                        print(f"Error converting price or quantity: {e}")
        return total_price
    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def save(self):
        self.session.modified = True



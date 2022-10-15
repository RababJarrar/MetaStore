
# Create your views here.

# Create your views here.

from django.conf import settings

from storeapp.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product_id] = int(quantity)
        else:
            self.cart[product_id] + int(quantity)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        quantity = self.cart.values()
        return sum(quantity)

    def get_total_price(self):
        total = 0
        for product_id, quantity in self.cart.items():
            product = Product.objects.get(id=product_id)
            total += product.price * quantity
        return total

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

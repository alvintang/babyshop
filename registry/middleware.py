from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth

from carton.cart import Cart


class AutoClearCart:
  def process_request(self, request):
    try:
      if datetime.now() - request.session['cart_last_touch'] > timedelta( 0, settings.AUTO_CLEARCART_DELAY * 60, 0):
        # clear cart here
        cart = Cart(request.session)
        for productItem in cart.items:
          print("product:"+productItem.product.name)
          print("quantity:"+str(productItem.quantity))
          print("price:"+str(productItem.price))
          productItem.product.quantity_bought -= productItem.quantity
          productItem.product.save()

        cart.clear()

        # print(request.session['cart_last_touch'])
        del request.session['cart_last_touch']
        return
    except KeyError:
      pass

    request.session['cart_last_touch'] = datetime.now()
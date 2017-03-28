import datetime
from decimal import Decimal
from django.utils import timezone
from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User, AnonymousUser

import paypalrestsdk
import logging

from cart import models
from cart.models import Cart, Item
from cart.cart import Cart
from cart.payments import Payments

class CartAndItemModelsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = RequestFactory()
        self.request.user = AnonymousUser()
        self.request.session = {}

    def _create_cart_in_database(self, creation_date=timezone.now(),
            checked_out=False):
        cart = models.Cart()
        cart.creation_date = creation_date
        cart.checked_out = False
        cart.save()
        return cart

    def _create_item_in_database(self, cart, product, quantity=1,
            unit_price=Decimal("100")):
        item = Item()
        item.cart = cart
        item.product = product
        item.quantity = quantity
        item.unit_price = unit_price
        item.save()
        return item

    def _create_user_in_database(self, name="buyer", password="password", email="user@user.com"):
        user = User(username=name, password=password, email=email)
        user.save()
        return user

    def test_cart_creation(self):
        print("Testing cart creation!")
        creation_date = timezone.now()
        cart = self._create_cart_in_database(creation_date)
        id = cart.id

        cart_from_database = models.Cart.objects.get(pk=id)
        self.assertEquals(cart, cart_from_database)
        print "Success!\n"


    def test_item_creation_and_association_with_cart(self):
        print("Testing item add to cart!")
        user = self._create_user_in_database()

        cart = self._create_cart_in_database()
        item = self._create_item_in_database(cart, user, quantity=1, unit_price=Decimal("100"))

        # get the first item in the cart
        item_in_cart = cart.item_set.all()[0]
        self.assertEquals(item_in_cart, item,
                "First item in cart should be equal the item we created")
        self.assertEquals(item_in_cart.product, user,
                "Product associated with the first item in cart should equal the user we're selling")
        self.assertEquals(item_in_cart.unit_price, Decimal("100"),
                "Unit price of the first item stored in the cart should equal 100")
        self.assertEquals(item_in_cart.quantity, 1,
                "The first item in cart should have 1 in it's quantity")
        print "Success!\n"


    def test_total_item_price(self):
        print("Testing total item price!")
        user = self._create_user_in_database()
        cart = self._create_cart_in_database()

        # not safe to do as the field is Decimal type. It works for integers but
        # doesn't work for float
        item_with_unit_price_as_integer = self._create_item_in_database(cart, product=user, quantity=3, unit_price=100)

        self.assertEquals(item_with_unit_price_as_integer.total_price, 300)

        # this is the right way to associate unit prices
        item_with_unit_price_as_decimal = self._create_item_in_database(cart,
                product=user, quantity=4, unit_price=Decimal("3.20"))
        self.assertEquals(item_with_unit_price_as_decimal.total_price, Decimal("12.80"))
        print "Success!\n"

    def test_update_cart(self):
        print("Testing update cart!")
        user = self._create_user_in_database()
        cart = Cart(self.request)
        cart.new(self.request)
        cart.add(product=user, quantity=3, unit_price=100)
        cart.update(product=user, quantity=2, unit_price=200)
        self.assertEquals(cart.summary(), 400)
        self.assertEquals(cart.count(), 2)
        print "Success!\n"

    def test_item_unicode(self):
        print("Testing item unicode!")
        user = self._create_user_in_database()
        cart = self._create_cart_in_database()
        item = self._create_item_in_database(cart, product=user, quantity=3, unit_price=Decimal("100"))
        self.assertEquals(item.__unicode__(), "3 units of User")
        print "Success!\n"
        
    def test_buy_cart(self):
        print("Testing buy cart!")
        cart = Cart(self.request)
        cart.new(self.request)
        cart.add(product=self._create_user_in_database("1"), quantity=3, unit_price=100)
        cart.add(product=self._create_user_in_database("2"), quantity=3, unit_price=100)
        cart.add(product=self._create_user_in_database("3"), quantity=3, unit_price=100)
        self.assertEquals(cart.summary(), 900)
        self.assertEquals(cart.count(), 9)
        paypal_payment = Payments(self.request)
        paypal_payment.buy(cart)
        print "Success!\n"
        
           
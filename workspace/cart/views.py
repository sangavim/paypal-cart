from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from cart import Cart
from .models import Product
from .payments import Payments

def add_to_cart(request, product_id, quantity):
    print "Add to cart: %s - %s" % (product_id, quantity)
    product = Product.objects.get(custom_id=product_id)
    cart = Cart(request)
    product_added = cart.add(product, product.price, quantity)
    url = reverse("index")
    if product_added == 1:
        request.session['status'] = "%s added to Cart!" % product.name
    else:
        request.session['status'] = "%s quantity updated in Cart!" % product.name
    return HttpResponseRedirect(url)

def remove_from_cart(request, product_id):
    print "Rremove from cart: %s" % (product_id) 
    product = Product.objects.get(custom_id=product_id)
    cart = Cart(request)
    product_removed = cart.remove(product)
    url = reverse("index")
    if product_removed:
        request.session['status'] = "%s removed from Cart!" % product.name
    else:
        request.session['status'] = "%s not in Cart!" % product.name
    return HttpResponseRedirect(url)

def index(request):
    cart = Cart(request)
    status = request.session.get('status','Welcome! Companies on Sale!')
    request.session['status'] = ""
    return render(request, 'index.html', {'cart' : cart, 'status' : status})
    
def get_cart(request):
    cart = Cart(request)
    request.session['status'] = ""
    return render(request, 'cart.html', {'cart' : cart})
    
def buy_cart(request):
    cart = Cart(request)
    url = reverse("index")
    if cart.is_empty():
        request.session['status'] = "Error: Cart empty!"
        return HttpResponseRedirect(url)
    
    paypal_payments = Payments(request)
    payment = paypal_payments.buy(cart)
    if payment.error:
        request.session['status'] = "Error: %s" % payment.error['details']
    else:
        request.session['status'] = "Success: Cart paid with PayPal. Payment ID: %s" % payment.id
        cart.clear()
    return HttpResponseRedirect(url)
    
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    request.session['status'] = "Cart cleared!"
    url = reverse("index")
    return HttpResponseRedirect(url)
    